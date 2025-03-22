from flask import Flask, request, send_file
import yt_dlp
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download_audio(youtube_url):
    """Downloads YouTube audio as MP3 and returns the file path."""
    output_path = os.path.join(DOWNLOAD_FOLDER, "audio.mp3")

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
        'outtmpl': output_path
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    return output_path

@app.route('/download', methods=['GET'])
def download():
    """API endpoint to download MP3 from YouTube."""
    url = request.args.get('url')
    if not url:
        return {"error": "No URL provided"}, 400

    try:
        audio_path = download_audio(url)
        return send_file(audio_path, as_attachment=True)
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
