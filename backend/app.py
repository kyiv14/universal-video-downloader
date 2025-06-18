from flask import Flask, request, send_file
import yt_dlp
import tempfile
import os

app = Flask(__name__)

@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return {"error": "No URL provided"}, 400

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "video.%(ext)s")
        ydl_opts = {
            'outtmpl': output_path,
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'quiet': True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                filename = os.path.splitext(filename)[0] + ".mp4"
                return send_file(filename, as_attachment=True, download_name="video.mp4")
        except Exception as e:
            return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run()
