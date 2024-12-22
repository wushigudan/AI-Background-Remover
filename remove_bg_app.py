import sys
import os
import requests
import traceback
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, 
                           QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QMessageBox, QLineEdit, QComboBox)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

def log(message):
    """打印日志到控制台和文件"""
    print(f"[BackgroundRemover] {message}")
    with open('background_remover.log', 'a', encoding='utf-8') as f:
        f.write(f"[BackgroundRemover] {message}\n")

# 设置环境变量
if getattr(sys, 'frozen', False):
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(sys._MEIPASS, 'PyQt5', 'Qt', 'plugins')
    log(f"使用打包环境，插件路径: {os.environ['QT_QPA_PLATFORM_PLUGIN_PATH']}")
else:
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(os.path.dirname(os.path.dirname(sys.executable)), 'Lib', 'site-packages', 'PyQt5', 'Qt', 'plugins')
    log(f"使用Python环境，插件路径: {os.environ['QT_QPA_PLATFORM_PLUGIN_PATH']}")

class BackgroundRemoverApp(QMainWindow):
    def __init__(self):
        super().__init__()
        log("初始化应用程序...")
        self.api_endpoints = {
            'Clipdrop': 'https://clipdrop-api.co/remove-background/v1',
            'Remove.bg': 'https://api.remove.bg/v1.0/removebg',
            'Photoroom': 'https://api.photoroom.com/v1/segment'
        }
        self.initUI()
        
    def initUI(self):
        log("初始化用户界面...")
        self.setWindowTitle('AI抠图工具')
        self.setGeometry(100, 100, 800, 600)
        
        # 创建主窗口部件和布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # 服务选择
        service_layout = QHBoxLayout()
        service_label = QLabel('选择服务:')
        self.service_combo = QComboBox()
        self.service_combo.addItems([
            'Clipdrop - 每月免费额度100次',
            'Remove.bg - 每月免费额度50次',
            'Photoroom - 每月免费额度10次'
        ])
        self.service_combo.currentIndexChanged.connect(self.on_service_changed)
        service_layout.addWidget(service_label)
        service_layout.addWidget(self.service_combo)
        layout.addLayout(service_layout)
        
        # API密钥输入
        api_layout = QHBoxLayout()
        api_label = QLabel('API Key:')
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText('请输入Clipdrop API Key')
        api_layout.addWidget(api_label)
        api_layout.addWidget(self.api_key_input)
        layout.addLayout(api_layout)
        
        # 尺寸选择
        size_layout = QHBoxLayout()
        size_label = QLabel('输出尺寸:')
        self.size_combo = QComboBox()
        size_layout.addWidget(size_label)
        size_layout.addWidget(self.size_combo)
        layout.addLayout(size_layout)
        
        # 初始化尺寸选项
        self.update_size_options()
        
        # 按钮布局
        button_layout = QHBoxLayout()
        
        # 选择图片按钮
        self.select_btn = QPushButton('选择图片', self)
        self.select_btn.clicked.connect(self.select_image)
        button_layout.addWidget(self.select_btn)
        
        # 开始处理按钮
        self.process_btn = QPushButton('开始抠图', self)
        self.process_btn.clicked.connect(self.process_image)
        self.process_btn.setEnabled(False)
        button_layout.addWidget(self.process_btn)
        
        # 保存结果按钮
        self.save_btn = QPushButton('保存结果', self)
        self.save_btn.clicked.connect(self.save_result)
        self.save_btn.setEnabled(False)
        button_layout.addWidget(self.save_btn)
        
        layout.addLayout(button_layout)
        
        # 图片显示区域
        image_layout = QHBoxLayout()
        
        # 原图显示
        self.original_label = QLabel('原始图片')
        self.original_label.setAlignment(Qt.AlignCenter)
        self.original_label.setMinimumSize(380, 380)
        self.original_label.setStyleSheet("border: 1px solid black")
        image_layout.addWidget(self.original_label)
        
        # 结果图显示
        self.result_label = QLabel('处理结果')
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setMinimumSize(380, 380)
        self.result_label.setStyleSheet("border: 1px solid black")
        image_layout.addWidget(self.result_label)
        
        layout.addLayout(image_layout)
        
        self.original_image_path = None
        self.result_image = None
        
    def update_size_options(self):
        """根据选择的服务更新尺寸选项"""
        self.size_combo.clear()
        service = self.service_combo.currentText().split(" ")[0]
        
        if service == "Clipdrop":
            self.size_combo.addItems([
                '标准清晰度',
                'HD - 1920x1080',
                '4K - 3840x2160'
            ])
        elif service == "Remove.bg":
            self.size_combo.addItems([
                'auto - 自动',
                'regular - 625x400',
                'full - 原图尺寸',
                '4k - 4000x4000'
            ])
        elif service == "Photoroom":
            self.size_combo.addItems([
                '标准 - 1024x1024',
                'HD - 2048x2048',
                '4K - 4096x4096'
            ])
            
    def on_service_changed(self, index):
        """当选择的服务改变时更新UI"""
        self.update_size_options()
        service = self.service_combo.currentText().split(" ")[0]
        self.api_key_input.setPlaceholderText(f'请输入{service} API Key')
            
    def select_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "选择图片", "", "图片文件 (*.png *.jpg *.jpeg)"
        )
        if file_name:
            # 检查文件大小
            file_size = os.path.getsize(file_name) / (1024 * 1024)  # 转换为MB
            log(f"选择的图片: {file_name}, 大小: {file_size:.2f}MB")
            
            if file_size > 12:
                log("图片大小超过限制")
                QMessageBox.warning(self, '警告', '图片大小超过12MB限制，请选择更小的图片')
                return
                
            self.original_image_path = file_name
            pixmap = QPixmap(file_name)
            scaled_pixmap = pixmap.scaled(360, 360, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.original_label.setPixmap(scaled_pixmap)
            self.process_btn.setEnabled(True)
            log("图片加载成功")
            
    def process_image(self):
        if not self.api_key_input.text():
            log("未输入API Key")
            QMessageBox.warning(self, '警告', '请输入API Key')
            return
            
        if not self.original_image_path:
            log("未选择图片")
            QMessageBox.warning(self, '警告', '请先选择图片')
            return
            
        service = self.service_combo.currentText().split(" ")[0]
        api_key = self.api_key_input.text()
        
        try:
            if service == "Clipdrop":
                self.process_with_clipdrop(api_key)
            elif service == "Remove.bg":
                self.process_with_remove_bg(api_key)
            elif service == "Photoroom":
                self.process_with_photoroom(api_key)
        except Exception as e:
            log(f"处理图片时发生错误: {str(e)}")
            error_msg = f'处理失败: {str(e)}\n\n'
            error_msg += '您可以尝试：\n'
            error_msg += '1. 检查网络连接\n'
            error_msg += '2. 确认API Key是否正确\n'
            error_msg += '3. 尝试使用其他服务'
            QMessageBox.critical(self, '错误', error_msg)
            
    def process_with_clipdrop(self, api_key):
        with open(self.original_image_path, 'rb') as image_file:
            response = requests.post(
                self.api_endpoints['Clipdrop'],
                files={'image_file': image_file},
                headers={'x-api-key': api_key}
            )
            
        self.handle_response(response)
        
    def process_with_remove_bg(self, api_key):
        size = self.size_combo.currentText().split(" ")[0]
        
        response = requests.post(
            self.api_endpoints['Remove.bg'],
            files={'image_file': open(self.original_image_path, 'rb')},
            data={'size': size},
            headers={'X-Api-Key': api_key},
        )
        
        self.handle_response(response)
        
    def process_with_photoroom(self, api_key):
        with open(self.original_image_path, 'rb') as image_file:
            response = requests.post(
                self.api_endpoints['Photoroom'],
                files={'image_file': image_file},
                headers={'x-api-key': api_key}
            )
            
        self.handle_response(response)
        
    def handle_response(self, response):
        log(f"API响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            log("处理成功")
            # 保存临时文件
            temp_result_path = 'temp_result.png'
            with open(temp_result_path, 'wb') as out:
                out.write(response.content)
                
            # 显示结果
            pixmap = QPixmap(temp_result_path)
            scaled_pixmap = pixmap.scaled(360, 360, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.result_label.setPixmap(scaled_pixmap)
            self.result_image = response.content
            self.save_btn.setEnabled(True)
            
            # 删除临时文件
            os.remove(temp_result_path)
            log("结果显示完成")
            
        elif response.status_code == 402:
            error_msg = '账户积分不足！\n\n'
            error_msg += '请确保您的账户有足够的免费额度或购买积分。\n'
            error_msg += '\n您可以尝试：\n'
            error_msg += '1. 使用其他服务\n'
            error_msg += '2. 创建新的API密钥\n'
            error_msg += '3. 购买服务积分'
            QMessageBox.critical(self, '错误', error_msg)
        else:
            error_msg = f'处理失败 (状态码: {response.status_code})\n'
            try:
                error_data = response.json()
                error_msg += f'\n错误详情：{str(error_data)}'
            except:
                error_msg += f'\n错误详情：{response.text}'
            QMessageBox.critical(self, '错误', error_msg)
        
    def save_result(self):
        if not self.result_image:
            QMessageBox.warning(self, '警告', '没有可保存的结果')
            return
            
        file_name, _ = QFileDialog.getSaveFileName(
            self, "保存结果", "", "PNG图片 (*.png)"
        )
        
        if file_name:
            with open(file_name, 'wb') as out:
                out.write(self.result_image)
            QMessageBox.information(self, '成功', '图片保存成功！')

if __name__ == '__main__':
    log("启动程序...")
    app = QApplication(sys.argv)
    ex = BackgroundRemoverApp()
    ex.show()
    sys.exit(app.exec_()) 
