from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import yt_dlp
import os
import uuid
import traceback

app = Flask(__name__)
CORS(app)  # Разрешаем кросс-доменные запросы

@app.route("/")
def home():
    return "🟢 Universal Video Downloader API is running!"

@app.route("/download", methods=["POST"])
def download():
    try:
        data = request.get_json()
        url = data.get("url")
        if not url:
            return jsonify({"error": "No URL provided"}), 400

        unique_id = str(uuid.uuid4())
        output_file = f"{unique_id}.mp4"

        ydl_opts = {
            "outtmpl": output_file,
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
            "cookies": "cookies.txt",  # Убедись, что cookies.txt лежит рядом с app.py
            "quiet": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return send_file(output_file, as_attachment=True)

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

    finally:
        # Удаляем файл после отправки (если он был создан)
        if 'output_file' in locals() and os.path.exists(output_file):
            os.remove(output_file)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
