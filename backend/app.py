from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import yt_dlp
import os
import uuid
import traceback

app = Flask(__name__)

# Разрешаем запросы с вашего фронта
CORS(app, origins=["https://universal-video-downloader.vercel.app"])

@app.route("/")
def home():
    return "✅ Universal Video Downloader API is running!"

@app.route("/download", methods=["POST"])
def download_video():
    try:
        data = request.get_json()
        url = data.get("url")
        if not url:
            return jsonify({"error": "Missing 'url' parameter"}), 400

        # Генерация уникального имени файла
        video_id = str(uuid.uuid4())
        filename = f"{video_id}.mp4"

        ydl_opts = {
            'outtmpl': filename,
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'cookies': 'cookies.txt',
            'quiet': True,
            'noplaylist': True
        }

        # Загрузка видео
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Отправка файла пользователю
        return send_file(filename, as_attachment=True)

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

    finally:
        # Удаление файла после отправки
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
