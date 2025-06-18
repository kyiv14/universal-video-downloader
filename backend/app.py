from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp
import os
import uuid

app = Flask(__name__)
CORS(app)

DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return 'YouTube Downloader API'

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'Missing URL'}), 400

    video_id = str(uuid.uuid4())
    output_template = os.path.join(DOWNLOAD_FOLDER, f'{video_id}.%(ext)s')

    ydl_opts = {
        'outtmpl': output_template,
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'cookies': 'cookies.txt',  # добавлено использование cookies
        'quiet': True,
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        # Поиск файла, чтобы отдать пользователю
        for ext in ['mp4', 'mkv', 'webm']:
            file_path = os.path.join(DOWNLOAD_FOLDER, f'{video_id}.{ext}')
            if os.path.exists(file_path):
                return send_file(file_path, as_attachment=True)
        return jsonify({'error': 'Download failed'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
