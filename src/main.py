import time
import pyperclip
import os
import re
import yt_dlp  # Ensure yt_dlp is imported
import json  # Import json to read the config file

def load_config():
    with open('config.json', 'r') as config_file:
        return json.load(config_file)

def sanitize_filename(filename):
    # Remove any characters that are not allowed in filenames
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def clean_url(url):
    return url.split('&')[0]  # URL encode the base URL

def download_youtube_audio(url, config):
    download_folder = config['download_folder']  # Use config value
    os.makedirs(download_folder, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio[ext=mp3]/bestaudio',  # Prioritize MP3 format, fallback to best audio
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',  # Directly convert to MP3
            'preferredquality': config['audio_quality'],  # Use config value
        }],
        'outtmpl': f'{download_folder}/%(title)s.%(ext)s',
        'ffmpeg_location': config['ffmpeg_location'],  # Use config value
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading: {url}")
            # Extract video information
            info_dict = ydl.extract_info(url, download=False)
            title = info_dict.get('title', 'Unknown Title')
            
            # Check if the file already exists
            file_path = os.path.join(download_folder, f"{sanitize_filename(title)}.mp3")
            if os.path.exists(file_path):
                print(f"File already exists: {file_path}")
                return
            
            # Download the audio
            ydl.download([url])
            print(f"Downloaded: {url}")
            
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")

def monitor_clipboard(config):
    previous_clipboard = pyperclip.paste()
    backlog = []

    while True:
        current_clipboard = pyperclip.paste()
        
        if current_clipboard != previous_clipboard:
            previous_clipboard = current_clipboard
            
            if "youtube.com/watch?v=" in current_clipboard or "youtu.be/" in current_clipboard:
                backlog.append(current_clipboard)
                print(f"Detected YouTube link: {current_clipboard}")
                
                while backlog:
                    next_url = backlog.pop(0)
                    download_youtube_audio(next_url, config)  # Pass config to the function
        
        time.sleep(config['clipboard_check_interval'])  # Use config value

if __name__ == "__main__":
    config = load_config()  # Load the configuration
    print("Starting clipboard monitoring...")
    monitor_clipboard(config)  # Pass config to the monitor function
