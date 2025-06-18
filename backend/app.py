from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import yt_dlp
import os
import uuid

app = Flask(__name__)

# Разрешить доступ только с нужного домена:
CORS(app, origins=["https://universal-video-downloader.vercel.app"])

@app.route("/")
def home():
    return "✅ Universal Video Downloader is running"

@app.route("/download", methods=["POST"])
def download_video():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL not provided"}), 400

    filename = f"video_{uuid.uuid4().hex}.mp4"

    ydl_opts = {
        "outtmpl": filename,
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "quiet": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return send_file(filename, as_attachment=True, download_name="video.mp4")
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == "__main__":
    # обязательно слушать 0.0.0.0 для Render и указать порт 10000
    app.run(host="0.0.0.0", port=10000)
