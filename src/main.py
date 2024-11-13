import time
import pyperclip
import os
import re
import yt_dlp
import json
import pandas as pd

def load_config():
    with open('config.json', 'r') as config_file:
        return json.load(config_file)

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def clean_url(url):
    return url.split('&')[0]

def download_youtube_audio(url, config):
    download_folder = config['download_folder']
    os.makedirs(download_folder, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio[ext=mp3]/bestaudio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': config['audio_quality'],
        }],
        'outtmpl': f'{download_folder}/%(title)s.%(ext)s',
        'ffmpeg_location': config['ffmpeg_location'],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading: {url}")
            info_dict = ydl.extract_info(url, download=False)
            title = info_dict.get('title', 'Unknown Title')
            file_path = os.path.join(download_folder, f"{sanitize_filename(title)}.mp3")
            if os.path.exists(file_path):
                print(f"File already exists: {file_path}")
                return
            ydl.download([url])
            print(f"Downloaded: {url}")
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")

def download_from_excel(config):
    excel_file = config.get('excel_file')
    if os.path.exists(excel_file):
        df = pd.read_excel(excel_file)
        if not df.empty:
            for index, row in df.iterrows():
                url = row[0]
                if isinstance(url, str) and ("youtube.com/watch?v=" in url or "youtu.be/" in url):
                    download_youtube_audio(url, config)
        else:
            print("The Excel file is empty.")
    else:
        print(f"Excel file not found: {excel_file}")

def monitor_clipboard(config):
    previous_clipboard = pyperclip.paste()
    backlog = []

    download_from_excel(config)

    while True:
        current_clipboard = pyperclip.paste()
        
        if current_clipboard != previous_clipboard:
            previous_clipboard = current_clipboard
            
            if "youtube.com/watch?v=" in current_clipboard or "youtu.be/" in current_clipboard:
                backlog.append(current_clipboard)
                print(f"Detected YouTube link: {current_clipboard}")
                
                while backlog:
                    next_url = backlog.pop(0)
                    download_youtube_audio(next_url, config)
        
        time.sleep(config['clipboard_check_interval'])

if __name__ == "__main__":
    config = load_config()
    print("Starting clipboard monitoring...")
    monitor_clipboard(config)
