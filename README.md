# AI-Background-Remover (AI智能抠图工具)

[English](#english) | [中文说明](#中文)

# English

A powerful AI-powered background removal tool that supports multiple popular AI services with a user-friendly interface.

## Features

- Multiple AI Services Support:
  - Clipdrop (Recommended): 100 free credits/month
  - Remove.bg: 50 free credits/month
  - Photoroom: 10 free credits/month
- Multiple output size options
- Real-time preview of original and processed images
- Save results in PNG format
- Image size limit: 12MB max

## Getting Started

1. Get API Key:
   - Clipdrop (Recommended):
     1. Visit https://clipdrop.co/apis
     2. Register/Login
     3. Get API key from API page
   
   - Remove.bg:
     1. Visit https://www.remove.bg/api
     2. Register/Login
     3. Get API key from API page
   
   - Photoroom:
     1. Visit https://www.photoroom.com/api
     2. Register/Login
     3. Get API key from API page

2. Usage Steps:
   1. Select service (Clipdrop by default)
   2. Enter the corresponding API key
   3. Select output size
   4. Click "Select Image" to choose an image
   5. Click "Process" to remove background
   6. Click "Save Result" to save the processed image

## Output Size Options

1. Clipdrop:
   - Standard Quality
   - HD - 1920x1080
   - 4K - 3840x2160

2. Remove.bg:
   - auto
   - regular - 625x400
   - full - original size
   - 4k - 4000x4000

3. Photoroom:
   - Standard - 1024x1024
   - HD - 2048x2048
   - 4K - 4096x4096

## Installation

1. Requirements:
   - Python 3.7+
   - PyQt5
   - requests

2. Install Dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run:
   ```bash
   python remove_bg_app.py
   ```

## Troubleshooting

1. Invalid API Key:
   - Check if API key is entered correctly
   - Verify if API key is activated
   - Check remaining free credits

2. Image Size Exceeded:
   - Ensure image is under 12MB
   - Compress image before processing

3. Network Error:
   - Check internet connection
   - Check proxy settings if needed

4. Insufficient Credits:
   - Check remaining free credits
   - Consider switching services
   - Purchase service credits

## Tips

1. Prefer Clipdrop Service:
   - Most free credits (100/month)
   - High quality results
   - Stable API

2. Image Processing Tips:
   - Compress large images before processing
   - Choose appropriate output size
   - Save important API keys

## Notes

1. API Usage:
   - Follow service terms
   - Use free credits wisely
   - Keep API keys secure

2. Image Requirements:
   - Supports PNG, JPG, JPEG
   - Max size: 12MB
   - Use clear original images
## Preview

![Interface](/11.jpg)
### Before and After
![Before-After](/4K.png)

---

# 中文

这是一个基于多个AI服务API的抠图工具，支持多种主流的AI抠图服务，界面简单易用。

## 功能特点

- 支持多个AI抠图服务：
  - Clipdrop（推荐）：每月免费额度100次
  - Remove.bg：每月免费额度50次
  - Photoroom：每月免费额度10次
- 支持多种输出尺寸选项
- 支持预览原图和处理结果
- 支持保存处理结果为PNG格式
- 图片大小限制：最大12MB

## 使用说明

1. 获取API密钥：
   - Clipdrop（推荐）：
     1. 访问 https://clipdrop.co/apis
     2. 注册/登录账号
     3. 在API页面获取API密钥
   
   - Remove.bg：
     1. 访问 https://www.remove.bg/api
     2. 注册/登录账号
     3. 在API页面获取API密钥
   
   - Photoroom：
     1. 访问 https://www.photoroom.com/api
     2. 注册/登录账号
     3. 在API页面获取API密钥

2. 使用步骤：
   1. 选择服务（默认为Clipdrop）
   2. 输入对应服务的API密钥
   3. 选择输出尺寸
   4. 点击"选择图片"按钮选择要处理的图片
   5. 点击"开始抠图"按钮进行处理
   6. 处理完成后可以点击"保存结果"保存处理后的图片

## 输出尺寸说明

1. Clipdrop：
   - 标准清晰度
   - HD - 1920x1080
   - 4K - 3840x2160

2. Remove.bg：
   - auto - 自动
   - regular - 625x400
   - full - 原图尺寸
   - 4k - 4000x4000

3. Photoroom：
   - 标准 - 1024x1024
   - HD - 2048x2048
   - 4K - 4096x4096

## 安装说明

1. 环境要求：
   - Python 3.7+
   - PyQt5
   - requests

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 运行程序：
   ```bash
   python remove_bg_app.py
   ```

## 常见问题

1. API密钥无效：
   - 检查API密钥是否正确输入
   - 确认API密钥是否已激活
   - 检查是否有足够的免费额度

2. 图片大小超限：
   - 确保图片小于12MB
   - 可以先压缩图片再处理

3. 网络连接错误：
   - 检查网络连接是否正常
   - 检查是否需要配置代理

4. 积分不足：
   - 检查账户剩余免费额度
   - 考虑更换其他服务
   - 购买服务积分

## 建议

1. 优先使用Clipdrop服务：
   - 每月免费额度最多（100次）
   - 处理质量好
   - API调用稳定

2. 图片处理建议：
   - 处理前压缩大图片
   - 选择合适的输出尺寸
   - 保存重要的API密钥

## 注意事项

1. API使用限制：
   - 请遵守各服务的使用条款
   - 合理使用免费额度
   - 注意API密钥安全

2. 图片要求：
   - 支持PNG、JPG、JPEG格式
   - 大小不超过12MB
   - 建议使用清晰的原图
  
   - ## 预览

![界面预览](/11.jpg)

### 效果对比
![效果对比](/4k.png)

## 技术支持

如有问题或建议，请提交Issue或联系开发者。 
