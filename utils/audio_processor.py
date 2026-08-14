import os
import shutil

import static_ffmpeg

static_ffmpeg.add_paths()

import yt_dlp
from pydub import AudioSegment

FFMPEG_PATH = shutil.which("ffmpeg")
FFPROBE_PATH = shutil.which("ffprobe")
FFMPEG_DIR = os.path.dirname(FFMPEG_PATH) if FFMPEG_PATH else None

DOWNLOAD_DIR = "downloades"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

AudioSegment.converter = FFMPEG_PATH
AudioSegment.ffmpeg = FFMPEG_PATH
AudioSegment.ffprobe = FFPROBE_PATH


def download_youtube_audio(url: str) -> str:
    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
        "nocheckcertificate": True,
        "geo_bypass": True,
        "nopart": True,       # Write directly to final file — avoids WinError 32 rename failures
        "overwrites": True,   # Overwrite if file already exists
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
        },
        "extractor_args": {
            "youtube": {
                "player_client": ["mweb", "android", "web"]
            }
        },
        "ffmpeg_location": FFMPEG_DIR,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
    except Exception as e:
        if "403" in str(e) or "Forbidden" in str(e):
            print("HTTP 403 encountered, retrying with fallback player client...")
            ydl_opts["extractor_args"] = {"youtube": {"player_client": ["ios", "web"]}}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
        else:
            raise e

    raw_filename = ydl.prepare_filename(info)
    base, _ = os.path.splitext(raw_filename)
    wav_path = base + ".wav"
    if not os.path.exists(wav_path):
        title = info.get("title", "")
        for f in os.listdir(DOWNLOAD_DIR):
            if f.endswith(".wav") and (title in f or os.path.splitext(f)[0] in title):
                wav_path = os.path.join(DOWNLOAD_DIR, f)
                break
    return wav_path


def convert_to_wav(input_path: str) -> str:
    """Convert any audio/video file to WAV format using pydub."""
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export(output_path, format="wav")
    return output_path


def chunk_audio(wav_path: str, chunk_minutes: int = 10) -> list:
    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_minutes * 60 * 1000

    chunks = []

    for i, start in enumerate(range(0, len(audio), chunk_ms)):
        chunk = audio[start : start + chunk_ms]
        if len(chunk) < 1000:  # Skip empty or near-empty segments under 1s
            continue
        chunk_path = f"{wav_path}_chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")

        chunks.append(chunk_path)

    if not chunks:
        chunks.append(wav_path)

    return chunks


def process_input(source: str) -> list:
    clean_source = source.strip()
    is_url = (
        clean_source.startswith("http://")
        or clean_source.startswith("https://")
        or "youtube.com" in clean_source
        or "youtu.be" in clean_source
    )
    if is_url:
        print("Detected YouTube URL. Downloading audio...")
        wav_path = download_youtube_audio(clean_source)
    elif os.path.exists(clean_source):
        print("Detected local file. Converting to WAV...")
        wav_path = convert_to_wav(clean_source)
    else:
        raise ValueError(
            "The input provided is neither a valid YouTube URL nor a file that exists on your computer. "
            "Please check the URL or file path and try again."
        )

    print("Chunking audio...")
    chunks = chunk_audio(wav_path)
    print(f"Audio ready — {len(chunks)} chunk(s) created.")
    return chunks
