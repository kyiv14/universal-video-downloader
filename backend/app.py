from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from yt_dlp import YoutubeDL
import os
import uuid

app = Flask(__name__)
CORS(app)

# Путь к cookies.txt
COOKIE_FILE = "cookies.txt"

@app.route("/")
def index():
    return "🎬 Media downloader is running!"

@app.route("/download", methods=["POST"])
def download_video():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    # Генерируем уникальное имя файла
    outtmpl = f"downloads/{uuid.uuid4()}.%(ext)s"

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": outtmpl,
        "noplaylist": True,
        "quiet": True,
        "cookiefile": COOKIE_FILE,
        "merge_output_format": "mp4"
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            # Если видео было объединено, расширение будет .mp4
            if not os.path.exists(filename):
                filename = os.path.splitext(filename)[0] + ".mp4"
            return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    os.makedirs("downloads", exist_ok=True)
    app.run(host="0.0.0.0", port=10000)
