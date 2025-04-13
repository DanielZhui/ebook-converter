import os
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
env_path = Path(__file__).parent.parent / '.env'
print("env_path", env_path)
load_dotenv(dotenv_path=env_path)

# 基础配置
SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# 文件路径配置
BASE_DIR = Path(__file__).parent
UPLOAD_FOLDER = BASE_DIR / os.getenv('UPLOAD_FOLDER', 'uploads')
DOWNLOAD_FOLDER = BASE_DIR / os.getenv('DOWNLOAD_FOLDER', 'downloads')

# 确保文件夹存在
UPLOAD_FOLDER.mkdir(exist_ok=True)
DOWNLOAD_FOLDER.mkdir(exist_ok=True)

# 允许的文件格式
ALLOWED_EXTENSIONS = {'epub', 'mobi', 'pdf',
                      'txt', 'azw', 'azw3', 'docx', 'html', 'rtf'}

# 支持的输出格式
OUTPUT_FORMATS = ['epub', 'mobi', 'pdf', 'txt', 'azw3', 'docx', 'html', 'rtf']

# 阿里云OSS配置
OSS_CONFIG = {
    'access_key_id': os.getenv('OSS_ACCESS_KEY_ID'),
    'access_key_secret': os.getenv('OSS_ACCESS_KEY_SECRET'),
    'endpoint': os.getenv('OSS_ENDPOINT'),
    'bucket_name': os.getenv('OSS_BUCKET_NAME'),
    'oss_folder': os.getenv('OSS_FOLDER', 'ebooks/'),
    'url_expiration': int(os.getenv('OSS_URL_EXPIRATION', 604800))  # 默认7天
}

# 阿里云邮件推送服务配置
ALIYUN_DM_CONFIG = {
    'access_key_id': os.getenv('DM_ACCESS_KEY_ID'),
    'access_key_secret': os.getenv('DM_ACCESS_KEY_SECRET'),
    'region': os.getenv('DM_REGION', 'cn-hangzhou'),
    'account_name': os.getenv('DM_ACCOUNT_NAME'),
    'from_alias': os.getenv('DM_FROM_ALIAS', '电子书格式转换服务'),
    'address_type': int(os.getenv('DM_ADDRESS_TYPE', 1)),
    'tag_name': os.getenv('DM_TAG_NAME', 'ebook_converter')
}
print(OSS_CONFIG)
