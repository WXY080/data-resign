from flask import Flask, jsonify, request, send_from_directory, render_template
import os
import shutil
from pathlib import Path

# 显式指定 templates 文件夹路径
app = Flask(__name__, template_folder='templates')

# 配置
BASE_DIR = Path.cwd()
IMAGE_DIR = BASE_DIR / "images"
GOOD_DIR = BASE_DIR / "正确"
BAD_DIR = BASE_DIR / "错误"

# 确保目录存在
for directory in [IMAGE_DIR, GOOD_DIR, BAD_DIR]:
    directory.mkdir(exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/images', methods=['GET'])
def get_images():
    images = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    return jsonify({'images': images, 'total': len(images)})


@app.route('/api/rate', methods=['POST'])
def rate_image():
    data = request.json
    image_name = data.get('image')
    rating = data.get('rating')

    if not image_name or not rating:
        return jsonify({'error': '缺少图片或评分'}), 400

    source_path = IMAGE_DIR / image_name
    if not source_path.exists():
        return jsonify({'error': '图片未找到'}), 404

    if rating == 'good':
        dest_path = GOOD_DIR / image_name
    elif rating == 'bad':
        dest_path = BAD_DIR / image_name
    else:
        return jsonify({'error': '无效评分'}), 400

    try:
        shutil.copy(str(source_path), str(dest_path))
        return jsonify({'message': '图片评分成功'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMAGE_DIR, filename)


if __name__ == '__main__':
    app.run(debug=True, port=5000)