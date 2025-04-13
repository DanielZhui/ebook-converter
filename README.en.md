# 📚 EBookConverter - E-book Format Conversion Service

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-brightgreen.svg)
![Flask](https://img.shields.io/badge/flask-2.0%2B-orange.svg)

A user-friendly web application for e-book format conversion, supporting multiple e-book formats and storing converted files in Alibaba Cloud OSS, with download links sent via Alibaba Cloud Direct Mail service.

## ✨ Features

- 🔄 Support for multiple e-book format conversions (EPUB, MOBI, PDF, TXT, AZW3, etc.)
- 🌐 Web-based interface, easy to use
- ☁️ Upload converted files to Alibaba Cloud OSS private bucket
- 📧 Send download links via Alibaba Cloud Direct Mail service
- 🔒 Generate temporary access URLs for file security
- 🧹 Automatic cleanup of expired files to save storage space
- 🔌 Configuration managed through environment variables for security

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Conversion Engine**: Calibre's ebook-convert
- **Cloud Services**: Alibaba Cloud OSS, Alibaba Cloud DirectMail
- **Configuration Management**: python-dotenv

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Calibre (providing ebook-convert tool)
- Alibaba Cloud account (OSS and DirectMail services)

### Installation Steps

1. **Clone Repository**

```bash
git clone https://github.com/DanielZhui/ebook-converter.git
cd ebook-converter
```

2. **Create and Activate Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure Environment Variables**

```bash
cp .env.example .env
# Edit .env file with your configuration
```

5. **Install Calibre**

Ensure Calibre is installed on your system and the `ebook-convert` command is available.

- Ubuntu: `sudo apt-get install calibre`
- macOS: `brew install --cask calibre`
- Windows: Download and install [Calibre](https://calibre-ebook.com/download)

6. **Run Application**

```bash
python app.py
```

7. **Access Application**

Open your browser and visit http://localhost:5000

## 🔧 Configuration

The application is configured through `.env` file or environment variables. Main configuration items include:

### Basic Configuration

```
SECRET_KEY=your_secret_key_here
DEBUG=False
```

### File Path Configuration

```
UPLOAD_FOLDER=uploads
DOWNLOAD_FOLDER=downloads
```

### Alibaba Cloud OSS Configuration

```
OSS_ACCESS_KEY_ID=your_access_key_id
OSS_ACCESS_KEY_SECRET=your_access_key_secret
OSS_ENDPOINT=https://oss-cn-hangzhou.aliyuncs.com
OSS_BUCKET_NAME=your-private-bucket-name
OSS_FOLDER=ebooks/
OSS_URL_EXPIRATION=604800  # 7 days, in seconds
```

### Alibaba Cloud Direct Mail Configuration

```
DM_ACCESS_KEY_ID=your_access_key_id
DM_ACCESS_KEY_SECRET=your_access_key_secret
DM_REGION=cn-hangzhou
DM_ACCOUNT_NAME=your_sender@example.com
DM_FROM_ALIAS=E-book Format Conversion Service
DM_ADDRESS_TYPE=1
DM_TAG_NAME=ebook_converter
```

## 📝 Usage Guide

1. Upload e-book file on the homepage
2. Select target format
3. (Optional) Check "Send download link to my email" and enter email address
4. Click "Start Conversion"
5. Wait for conversion to complete, download file or check email for download link

## 🌟 Preview

![fa065f878a3aeda81f30678bfb8c1ebd.png](https://i.miji.bid/2025/03/18/fa065f878a3aeda81f30678bfb8c1ebd.png)
![3574d6be32a6617b1d66511a237b1b9c.png](https://i.miji.bid/2025/03/18/3574d6be32a6617b1d66511a237b1b9c.png)

## 🔄 Workflow

1. User uploads e-book file and selects target format
2. Application uses Calibre's `ebook-convert` tool for format conversion
3. Converted file is uploaded to Alibaba Cloud OSS private bucket
4. Generate temporary access URL with expiration
5. (If selected by user) Send email with download link via Alibaba Cloud DirectMail
6. Local files are automatically cleaned up after 24 hours

## 🛡️ Security

- All sensitive configurations managed through environment variables, not hardcoded in source code
- OSS uses private bucket, files not publicly accessible
- Download links have expiration time, default 7 days
- Regular cleanup of local temporary files

## 📋 Todo List

- [ ] Add user authentication system
- [ ] Support more e-book formats
- [ ] Add batch conversion feature
- [ ] Implement conversion history feature
- [ ] Add file preview feature

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📬 Contact

For questions or suggestions, please [submit an Issue](https://github.com/yourusername/ebook-converter/issues).

---

⭐ If you find this project useful, please give it a Star! ⭐