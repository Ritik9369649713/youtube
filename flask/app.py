from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)  # Allow frontend requests from different domains

DOWNLOAD_PATH = "downloads"

if not os.path.exists(DOWNLOAD_PATH):
    os.makedirs(DOWNLOAD_PATH)

@app.route("/download", methods=["POST"])
def download_video():
    try:
        data = request.get_json()
        video_url = data.get("url")

        if not video_url:
            return jsonify({"error": "No URL provided"}), 400

        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
            'outtmpl': f"{DOWNLOAD_PATH}/video.mp4",
            'merge_output_format': 'mp4'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        return send_file(f"{DOWNLOAD_PATH}/video.mp4", as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
