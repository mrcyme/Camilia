"""
- WEBPARSER
- GOOGLESEARCH
- SUMMARIZER
- Dowload and transcript
"""
from yt_dlp import YoutubeDL



def download_audio(url, output_path= "./download"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_path,  # Save the file with the specified name
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return f"{output_path}.mp3"



