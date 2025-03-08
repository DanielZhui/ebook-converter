import os
import uuid
import subprocess
from flask import Flask, render_template, request, send_from_directory, redirect, url_for, flash
from werkzeug.utils import secure_filename
import shutil
import logging
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'abcABC123!@#'

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 确保文件夹存在
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
DOWNLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# 允许的文件格式
ALLOWED_EXTENSIONS = {'epub', 'mobi', 'pdf', 'txt', 'azw', 'azw3', 'docx', 'html', 'rtf'}

# 支持的输出格式
OUTPUT_FORMATS = ['epub', 'mobi', 'pdf', 'txt', 'azw3', 'docx', 'html', 'rtf']

def allowed_file(filename):
    print(filename)
    return '.' in filename and filename.rsplit('.', 1)[-1].lower() in ALLOWED_EXTENSIONS

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
    # filename = secure_filename(file.filename)
    filename = file.filename
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
    output_path = os.path.join(DOWNLOAD_FOLDER, f"{unique_id}_{output_filename}")

    try:
        # 使用 Calibre 的 ebook-convert 进行转换
        cmd = ['ebook-convert', input_path, output_path]
        logger.info(f"执行命令: {' '.join(cmd)}")

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            logger.error(f"转换失败: {stderr.decode('utf-8')}")
            flash(f'转换失败: {stderr.decode("utf-8")}')
            os.remove(input_path)
            return redirect(request.url)

        logger.info(f"转换成功: {input_path} -> {output_path}")

        # 删除上传的文件
        os.remove(input_path)

        # 重定向到下载页面
        return redirect(url_for('download_file', filename=f"{unique_id}_{output_filename}"))

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
    return render_template('result.html', filename=filename)

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
            file_creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
            if (current_time - file_creation_time).days >= 1:
                os.remove(file_path)
                logger.info(f"已删除旧文件: {file_path}")

# 每次启动应用时清理旧文件
cleanup_old_files()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)