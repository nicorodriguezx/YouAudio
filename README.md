# YouAudio

A simple Python application that monitors your clipboard for YouTube links and automatically downloads the audio in your preferred format. This project uses `yt-dlp` for downloading and `ffmpeg` for audio processing.

## Features

- Monitors clipboard for YouTube links.
- Downloads audio in MP3 format.
- Reads YouTube links from a specified Excel file and downloads them automatically.
- Configurable download folder and audio quality.
- Supports various audio formats.


## Requirements

- Python 3.8 or higher
- `yt-dlp`
- `pyperclip`
- `pandas`
- `openpyxl`
- `ffmpeg` (make sure it's installed and accessible in your system's PATH)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/YouAudio.git
   cd YouAudio
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Make sure `ffmpeg` is installed. You can download it from [FFmpeg's official website](https://ffmpeg.org/download.html).

## Configuration

Create a `config.json` file in the project root with the following structure:

```json
{
    "download_folder": "C:/Downloads",  // Where the downloaded audio files will be saved
    "ffmpeg_location": "C:/ffmpeg/bin",  // Path to the FFmpeg binary
    "audio_format": "mp3",                // Desired audio format (allowed formats: mp3, aac, alac, flac, m4a, opus, vorbis, wav)
    "audio_quality": "192",                // Audio quality (allowed values: 0-10 for VBR or specific bitrates like 128K, 192K, 320K)
    "clipboard_check_interval": 1,          // Interval (in seconds) to check the clipboard
    "excel_file": "C:/Downloads/to_download.xlsx"  // Specify the full path to the Excel file containing YouTube links
}
```

## Usage

1. Run the application:

   ```bash
   python src/main.py
   ```

2. The application will first check for YouTube links in the specified Excel file (e.g., `to_download.xlsx`) and download them automatically.

3. After processing the Excel file, copy a YouTube link to your clipboard. The application will automatically detect the link and start downloading the audio.

4. The downloaded audio files will be saved in the specified download folder.

## Example Configuration

Here’s an example of a `config.json` file:

```json
{
    "download_folder": "C:/Downloads",
    "ffmpeg_location": "C:/ffmpeg/bin",
    "audio_format": "mp3",
    "audio_quality": "192",
    "clipboard_check_interval": 1,
    "excel_file": "C:/Downloads/to_download.xlsx"  // Specify the full path to the Excel file with YouTube links
}
```

## Notes

- Ensure that the paths in the configuration file are correct and that the folders exist.
- The application will check the clipboard every second for new YouTube links.
- If an Excel file specified in the configuration is present, the application will download all YouTube links listed in it before monitoring the clipboard.

## License

This project is licensed under the UNLICENSE. See the [UNLICENSE](UNLICENSE) file for details.

## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for the powerful downloading capabilities.
- [FFmpeg](https://ffmpeg.org/) for audio processing.