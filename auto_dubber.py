"""
Video to Subtitle & Dubbing Converter
-------------------------------------
Created by: Muhammed Galal
GitHub: https://github.com/your_github_username
License: MIT License

Description:
This script extracts audio from video files, transcribes it into text using Whisper, 
generates an SRT subtitle file, translates it into Arabic, converts Arabic subtitles into speech,
and merges the generated voice with the original video.

Requirements:
- whisper
- moviepy
- tqdm
- deep_translator
- gTTS

Run:
$ python script.py
"""

import os
import whisper
import moviepy.editor as mp
from tqdm import tqdm
from deep_translator import GoogleTranslator
from gtts import gTTS

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
        arabic_text = ""
        for line in lines:
            if "-->" in line or line.strip().isdigit() or line.strip() == "":
                translated_lines.append(line)
            else:
                translated_text = translator.translate(line.strip())
                translated_lines.append(translated_text + "\n")
                arabic_text += translated_text + " "
        with open(translated_srt_path, "w", encoding="utf-8") as f:
            f.writelines(translated_lines)
        return arabic_text
    except Exception as e:
        print(f"Error translating {srt_path}: {e}")
        return ""

def generate_dubbed_audio(text, audio_output_path):
    """Converts Arabic text into speech and saves it as a WAV file."""
    try:
        tts = gTTS(text=text, lang="ar")
        tts.save(audio_output_path)
        print(f"Dubbed audio saved: {audio_output_path}")
    except Exception as e:
        print(f"Error generating dubbed audio: {e}")

def merge_audio_with_video(video_path, dubbed_audio_path, output_video_path):
    """Merges the generated dubbed audio with the original video."""
    try:
        video = mp.VideoFileClip(video_path)
        dubbed_audio = mp.AudioFileClip(dubbed_audio_path)
        if dubbed_audio.duration < video.duration:
            dubbed_audio = mp.concatenate_audioclips([dubbed_audio] * int(video.duration / dubbed_audio.duration + 1))
            dubbed_audio = dubbed_audio.subclip(0, video.duration)
        video = video.set_audio(dubbed_audio)
        video.write_videofile(output_video_path, codec="libx264", audio_codec="aac")
        print(f"Dubbed video saved: {output_video_path}")
        os.remove(dubbed_audio_path)  # حذف ملف الصوت المدبلج بعد الاستخدام
    except Exception as e:
        print(f"Error merging audio with video: {e}")

def process_videos(folder_path):
    """Processes all video files in a folder: extracts audio, transcribes it, saves subtitles, translates them, generates dubbed audio, and merges it with the video."""
    model = whisper.load_model("base")
    video_files = [f for f in os.listdir(folder_path) if f.endswith(('.mp4', '.avi', '.mov', '.mkv'))]
    if not video_files:
        print("No video files found in the specified folder.")
        return
    for video in tqdm(video_files, desc="Processing Videos"):
        video_path = os.path.join(folder_path, video)
        audio_path = video_path.rsplit(".", 1)[0] + ".wav"
        srt_path = video_path.rsplit(".", 1)[0] + ".srt"
        translated_srt_path = video_path.rsplit(".", 1)[0] + "_ar.srt"
        dubbed_audio_path = video_path.rsplit(".", 1)[0] + "_dubbed.mp3"
        output_video_path = video_path.rsplit(".", 1)[0] + "_dubbed.mp4"
        extract_audio(video_path, audio_path)
        segments = transcribe_audio(audio_path, model)
        if segments:
            save_srt(segments, srt_path)
            arabic_text = translate_srt(srt_path, translated_srt_path)
            if arabic_text:
                generate_dubbed_audio(arabic_text, dubbed_audio_path)
                merge_audio_with_video(video_path, dubbed_audio_path, output_video_path)
        os.remove(audio_path)
        print(f"Processed: {video} -> {srt_path}, {translated_srt_path}, {output_video_path}")

if __name__ == "__main__":
    folder_path = input("Enter the folder path: ").strip()
    if os.path.isdir(folder_path):
        process_videos(folder_path)
    else:
        print("Invalid folder path. Please enter a valid directory.")
