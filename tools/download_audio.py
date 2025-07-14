import yt_dlp
import re

def extract_video_id(url):
 
    match = re.search(r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})", url)
    return match.group(1) if match else "audio"



def download_audio(url):
    print(url)
    video_id = extract_video_id(url)
    print(video_id)
    output_path = f"audio_{video_id}.mp3"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f"audio_{video_id}.%(ext)s",
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print("Audio downloaded to:", output_path)
    return output_path