from flask import Flask, request, render_template, send_file
import yt_dlp
import os

app = Flask(__name__)

# إنشاء مجلد التنزيلات
DOWNLOAD_DIR = "downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download_video():
    url = request.form.get("url")
    quality = request.form.get("quality", "best")

    if not url:
        return "Please provide a valid URL", 400

    ydl_opts = {
        "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
        "format": quality,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info)
            return send_file(file_name, as_attachment=True)
    except yt_dlp.utils.DownloadError as e:
        return f"Error: Unable to download video. Details: {e}", 500
    except Exception as e:
        return f"Error: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
