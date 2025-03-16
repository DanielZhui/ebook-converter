import oss2
from utils.logger import logger
from config import OSS_CONFIG

def upload_to_oss(local_file_path, file_name):
    """上传文件到阿里云OSS并返回临时访问URL"""
    try:
        # 初始化OSS客户端
        auth = oss2.Auth(OSS_CONFIG['access_key_id'], OSS_CONFIG['access_key_secret'])
        bucket = oss2.Bucket(auth, OSS_CONFIG['endpoint'], OSS_CONFIG['bucket_name'])

        # OSS中的文件路径
        oss_file_path = OSS_CONFIG['oss_folder'] + file_name

        # 上传文件
        with open(local_file_path, 'rb') as file_obj:
            bucket.put_object(oss_file_path, file_obj)

        logger.info(f"文件已上传到OSS: {oss_file_path}")

        # 生成临时访问URL
        url = bucket.sign_url('GET', oss_file_path, OSS_CONFIG['url_expiration'])

        return {
            'success': True,
            'url': url,
            'oss_path': oss_file_path,
            'expiration_days': OSS_CONFIG['url_expiration'] // (24 * 3600)
        }
    except Exception as e:
        logger.error(f"上传到OSS失败: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }
