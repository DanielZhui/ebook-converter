# 📚 EBookConverter - 电子书格式转换服务

[English](README.en.md) | 简体中文

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-brightgreen.svg)
![Flask](https://img.shields.io/badge/flask-2.0%2B-orange.svg)

一个简单易用的电子书格式转换Web应用，支持多种电子书格式互相转换，并可将转换后的文件存储到阿里云OSS，通过阿里云邮件推送服务发送下载链接。

## ✨ 功能特点

- 🔄 支持多种电子书格式互相转换 (EPUB, MOBI, PDF, TXT, AZW3等)
- 🌐 基于Web界面，简单易用
- ☁️ 将转换后的文件上传到阿里云OSS私有Bucket
- 📧 通过阿里云邮件推送服务发送下载链接
- 🔒 生成临时访问URL，保障文件安全
- 🧹 自动清理过期文件，节省存储空间
- 🔌 配置信息通过环境变量管理，安全可靠

## 🛠️ 技术栈

- **后端**: Flask (Python)
- **前端**: HTML, CSS, JavaScript, Bootstrap 5
- **转换引擎**: Calibre's ebook-convert
- **云服务**: 阿里云OSS, 阿里云DirectMail
- **配置管理**: python-dotenv

## 🚀 快速开始

### 前提条件

- Python 3.8+
- Calibre (提供ebook-convert工具)
- 阿里云账号 (OSS和DirectMail服务)

### 安装步骤

1. **克隆仓库**

```bash
git clone https://github.com/DanielZhui/ebook-converter.git
cd ebook-converter
```

2. **创建并激活虚拟环境**

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **安装依赖**

```bash
pip install -r requirements.txt
```

4. **配置环境变量**

```bash
cp .env.example .env
# 编辑.env文件，填入您的配置信息
```

5. **安装Calibre**

确保您的系统中已安装Calibre，并且`ebook-convert`命令可用。

- Ubuntu: `sudo apt-get install calibre`
- macOS: `brew install --cask calibre`
- Windows: 下载并安装[Calibre](https://calibre-ebook.com/download)

6. **运行应用**

```bash
python app.py
```

7. **访问应用**

打开浏览器访问 http://localhost:5000

## 🔧 配置说明

应用通过`.env`文件或环境变量进行配置。主要配置项包括：

### 基础配置

```
SECRET_KEY=your_secret_key_here
DEBUG=False
```

### 文件路径配置

```
UPLOAD_FOLDER=uploads
DOWNLOAD_FOLDER=downloads
```

### 阿里云OSS配置

```
OSS_ACCESS_KEY_ID=your_access_key_id
OSS_ACCESS_KEY_SECRET=your_access_key_secret
OSS_ENDPOINT=https://oss-cn-hangzhou.aliyuncs.com
OSS_BUCKET_NAME=your-private-bucket-name
OSS_FOLDER=ebooks/
OSS_URL_EXPIRATION=604800  # 7天，单位秒
```

### 阿里云邮件推送服务配置

```
DM_ACCESS_KEY_ID=your_access_key_id
DM_ACCESS_KEY_SECRET=your_access_key_secret
DM_REGION=cn-hangzhou
DM_ACCOUNT_NAME=your_sender@example.com
DM_FROM_ALIAS=电子书格式转换服务
DM_ADDRESS_TYPE=1
DM_TAG_NAME=ebook_converter
```

## 📝 使用说明

1. 在首页上传电子书文件
2. 选择目标格式
3. (可选) 勾选"发送下载链接到我的邮箱"并输入邮箱地址
4. 点击"开始转换"
5. 等待转换完成，下载文件或查收邮件中的下载链接

## 🌟 预览

![fa065f878a3aeda81f30678bfb8c1ebd.png](https://i.miji.bid/2025/03/18/fa065f878a3aeda81f30678bfb8c1ebd.png)
![3574d6be32a6617b1d66511a237b1b9c.png](https://i.miji.bid/2025/03/18/3574d6be32a6617b1d66511a237b1b9c.png)

## 🔄 工作流程

1. 用户上传电子书文件并选择目标格式
2. 应用使用Calibre的`ebook-convert`工具进行格式转换
3. 转换后的文件被上传到阿里云OSS私有Bucket
4. 生成带有时效性的临时访问URL
5. (如果用户选择) 通过阿里云DirectMail发送包含下载链接的邮件
6. 本地文件在24小时后自动清理

## 🛡️ 安全性

- 所有敏感配置通过环境变量管理，不硬编码在源代码中
- OSS使用私有Bucket，文件不可公开访问
- 下载链接有时效性，默认7天后过期
- 本地临时文件定期清理

## 📋 待办事项

- [ ] 添加用户认证系统
- [ ] 支持更多电子书格式
- [ ] 添加批量转换功能
- [ ] 实现转换历史记录功能
- [ ] 添加文件预览功能

## 🤝 贡献

欢迎贡献代码、报告问题或提出新功能建议！请先Fork仓库，然后提交Pull Request。

## 📄 许可证

本项目采用MIT许可证 - 详见[LICENSE](LICENSE)文件。

## 📬 联系方式

如有问题或建议，请[提交Issue](https://github.com/yourusername/ebook-converter/issues)。

---

⭐ 如果您觉得这个项目有用，请给它一个Star! ⭐