"""
Video to Subtitle Converter
---------------------------
Created by: Muhammed Galal
GitHub: https://github.com/your_github_username
License: MIT License

Description:
This script extracts audio from video files, transcribes it into text using Whisper, 
generates an SRT subtitle file, and translates it into Arabic.

Requirements:
- whisper
- moviepy
- tqdm
- deep_translator

Run:
$ python script.py
"""

import os
import whisper
import moviepy.editor as mp
from tqdm import tqdm
from deep_translator import GoogleTranslator


def extract_audio(video_path, audio_path):
    """Extracts audio from a video file and saves it as a WAV file."""
    try:
        video = mp.VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path, codec='pcm_s16le')
    except Exception as e:
        print(f"Error extracting audio from {video_path}: {e}")


def transcribe_audio(audio_path, model):
    """Transcribes audio using the Whisper model."""
    try:
        result = model.transcribe(audio_path)
        return result["segments"]
    except Exception as e:
        print(f"Error transcribing {audio_path}: {e}")
        return []


def save_srt(segments, srt_path):
    """Saves transcribed text into an SRT subtitle file."""
    try:
        with open(srt_path, "w", encoding="utf-8") as f:
            for i, segment in enumerate(segments, start=1):
                start = segment['start']
                end = segment['end']
                text = segment['text']

                start_srt = f"{int(start // 3600):02}:{int((start % 3600) // 60):02}:{int(start % 60):02},{int((start % 1) * 1000):03}"
                end_srt = f"{int(end // 3600):02}:{int((end % 3600) // 60):02}:{int(end % 60):02},{int((end % 1) * 1000):03}"

                f.write(f"{i}\n{start_srt} --> {end_srt}\n{text}\n\n")
    except Exception as e:
        print(f"Error saving SRT file {srt_path}: {e}")


def translate_srt(srt_path, translated_srt_path):
    """Translates an SRT file from English to Arabic."""
    try:
        translator = GoogleTranslator(source="en", target="ar")

        with open(srt_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        translated_lines = []
        for line in lines:
            if "-->" in line or line.strip().isdigit() or line.strip() == "":
                translated_lines.append(line)  # Don't translate timestamps or numbers
            else:
                translated_text = translator.translate(line.strip())
                translated_lines.append(translated_text + "\n")

        with open(translated_srt_path, "w", encoding="utf-8") as f:
            f.writelines(translated_lines)
    except Exception as e:
        print(f"Error translating {srt_path}: {e}")


def process_videos(folder_path):
    """Processes all video files in a folder: extracts audio, transcribes it, saves subtitles, and translates them."""
    model = whisper.load_model("base")  # Change to "small", "medium", or "large" for better accuracy
    video_files = [f for f in os.listdir(folder_path) if f.endswith(('.mp4', '.avi', '.mov', '.mkv'))]

    if not video_files:
        print("No video files found in the specified folder.")
        return

    for video in tqdm(video_files, desc="Processing Videos"):
        video_path = os.path.join(folder_path, video)
        audio_path = video_path.rsplit(".", 1)[0] + ".wav"
        srt_path = video_path.rsplit(".", 1)[0] + ".srt"
        translated_srt_path = video_path.rsplit(".", 1)[0] + "_ar.srt"  # Arabic subtitle file

        extract_audio(video_path, audio_path)
        segments = transcribe_audio(audio_path, model)
        if segments:
            save_srt(segments, srt_path)
            translate_srt(srt_path, translated_srt_path)

        os.remove(audio_path)  # Delete audio file after processing
        print(f"Processed: {video} -> {srt_path} & {translated_srt_path}")


if __name__ == "__main__":
    folder_path = input("Enter the folder path: ").strip()
    if os.path.isdir(folder_path):
        process_videos(folder_path)
    else:
        print("Invalid folder path. Please enter a valid directory.")
