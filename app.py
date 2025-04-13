import os
import uuid
import subprocess
from flask import Flask, render_template, request, send_from_directory, redirect, url_for, flash
from werkzeug.utils import secure_filename
from utils.logger import logger
from datetime import datetime, timedelta
import re
from services.aliyun_email import AliyunEmailService
from services.oss import upload_to_oss

from config import (
    SECRET_KEY, DEBUG, UPLOAD_FOLDER, DOWNLOAD_FOLDER,
    ALLOWED_EXTENSIONS, OUTPUT_FORMATS, OSS_CONFIG
)

app = Flask(__name__)
app.secret_key = SECRET_KEY

# 确保文件夹存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[-1].lower() in ALLOWED_EXTENSIONS


def is_valid_email(email):
    """验证邮箱格式是否正确"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


@app.route('/')
def index():
    return render_template('index.html', formats=OUTPUT_FORMATS)


@app.route('/convert', methods=['POST'])
def convert_file():
    # 检查是否有文件
    if 'file' not in request.files:
        flash('没有选择文件')
        return redirect(request.url)

    file = request.files['file']

    # 如果用户没有选择文件
    if file.filename == '':
        flash('没有选择文件')
        return redirect(request.url)

    # 检查文件格式是否允许
    if not allowed_file(file.filename):
        flash(f'不支持的文件格式。允许的格式: {", ".join(ALLOWED_EXTENSIONS)}')
        return redirect(request.url)

    # 安全地保存文件
    filename = secure_filename(file.filename)
    unique_id = str(uuid.uuid4())
    input_path = os.path.join(UPLOAD_FOLDER, f"{unique_id}_{filename}")
    file.save(input_path)

    # 获取目标格式
    output_format = request.form.get('format')
    if output_format not in OUTPUT_FORMATS:
        flash(f'不支持的输出格式。允许的格式: {", ".join(OUTPUT_FORMATS)}')
        os.remove(input_path)  # 删除上传的文件
        return redirect(request.url)

    # 创建输出文件路径
    output_filename = f"{os.path.splitext(filename)[0]}.{output_format}"
    unique_output_filename = f"{unique_id}_{output_filename}"
    output_path = os.path.join(DOWNLOAD_FOLDER, unique_output_filename)

    # 获取邮箱信息（如果提供）
    send_to_email = request.form.get('send_to_email', '').strip()
    send_email_enabled = request.form.get('send_email_enabled') == 'on'

    # 验证邮箱格式（如果启用了邮件发送）
    if send_email_enabled and send_to_email and not is_valid_email(send_to_email):
        flash('请输入有效的邮箱地址')
        os.remove(input_path)
        return redirect(request.url)

    try:
        # 使用 Calibre 的 ebook-convert 进行转换
        cmd = ['ebook-convert', input_path, output_path]
        logger.info(f"执行命令: {' '.join(cmd)}")

        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            logger.error(f"转换失败: {stderr.decode('utf-8')}")
            flash(f'转换失败: {stderr.decode("utf-8")}')
            os.remove(input_path)
            return redirect(request.url)

        logger.info(f"转换成功: {input_path} -> {output_path}")

        # 删除上传的文件
        os.remove(input_path)

        # 上传到OSS的变量
        oss_upload_result = None

        # 如果启用了邮件发送并且提供了邮箱
        email_sent = False
        if send_email_enabled and send_to_email:
            # 上传文件到OSS
            oss_upload_result = upload_to_oss(
                output_path, unique_output_filename)

            if oss_upload_result['success']:
                # 构建邮件内容
                subject = f"您的电子书 {os.path.splitext(filename)} 已转换完成"
                expiration_date = (datetime.now(
                ) + timedelta(days=oss_upload_result['expiration_days'])).strftime('%Y-%m-%d %H:%M:%S')

                html_body = f"""
                <html>
                <body>
                    <h2>电子书格式转换完成</h2>
                    <p>您好，</p>
                    <p>您的电子书 <strong>{filename}</strong> 已成功转换为 <strong>{output_format.upper()}</strong> 格式。</p>
                    <p>您可以通过以下链接下载转换后的电子书：</p>
                    <p><a href="{oss_upload_result['url']}" target="_blank">点击这里下载电子书</a></p>
                    <p><strong>注意：</strong> 此链接将在 {oss_upload_result['expiration_days']} 天后（{expiration_date}）过期。</p>
                    <p>感谢您使用我们的电子书转换服务！</p>
                    <p>此邮件由系统自动发送，请勿回复。</p>
                </body>
                </html>
                """

                # 发送邮件
                email_sent = AliyunEmailService.single_send_mail(
                    send_to_email, subject, html_body)

                if email_sent:
                    logger.info(f"邮件已成功发送到 {send_to_email}")
                else:
                    logger.error(f"邮件发送失败")

        # 重定向到下载页面
        return redirect(url_for('download_file',
                                filename=unique_output_filename,
                                email=send_to_email if email_sent else '',
                                email_sent=str(email_sent),
                                oss_url=oss_upload_result['url'] if oss_upload_result and oss_upload_result['success'] else ''))

    except Exception as e:
        logger.error(f"发生错误: {str(e)}")
        flash(f'转换过程中发生错误: {str(e)}')
        # 清理文件
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)
        return redirect(request.url)


@app.route('/download/<filename>')
def download_file(filename):
    email = request.args.get('email', '')
    email_sent = request.args.get('email_sent', 'False') == 'True'
    oss_url = request.args.get('oss_url', '')
    return render_template('result.html',
                           filename=filename,
                           email=email,
                           email_sent=email_sent,
                           oss_url=oss_url,
                           expiration_days=OSS_CONFIG['url_expiration'] // (24 * 3600))


@app.route('/get-file/<filename>')
def get_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

# 定期清理下载目录中的旧文件


def cleanup_old_files():
    current_time = datetime.now()
    for filename in os.listdir(DOWNLOAD_FOLDER):
        file_path = os.path.join(DOWNLOAD_FOLDER, filename)
        # 如果文件超过24小时，则删除
        if os.path.isfile(file_path):
            file_creation_time = datetime.fromtimestamp(
                os.path.getctime(file_path))
            if (current_time - file_creation_time).days >= 1:
                os.remove(file_path)
                logger.info(f"已删除旧文件: {file_path}")


# 每次启动应用时清理旧文件
cleanup_old_files()

if __name__ == '__main__':
    app.run(debug=DEBUG, host='0.0.0.0', port=5001)
