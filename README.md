# video-subtitle-converter
Video Subtitle & Dubbing Converter

Description
This project provides two Python scripts for processing video files:
1. video_to_srt.py: Extracts audio from video, transcribes it using Whisper, and generates SRT subtitle files in both English and Arabic.
2. auto_dubber.py: Performs the same operations as video_to_srt.py, but also generates Arabic voice dubbing and merges it with the video.

Features

✅ Convert video to subtitles (.srt) <br>
✅ Transcribe audio using Whisper (local model, no API required) <br>
✅ Translate subtitles from English to Arabic <br>
✅ Generate Arabic voice dubbing using gTTS <br>
✅ Merge dubbed audio with video <br>
✅ Supports multiple video formats: .mp4, .avi, .mov, .mkv <br>

Installation

1️⃣ Clone the Repository
```
$ git clone https://github.com/your_github_username/video-subtitle-converter.git
$ cd video-subtitle-converter
```
2️⃣ Install Dependencies

Make sure you have Python installed (Python 3.8+ recommended). Then, run:
```
$ pip install -r requirements.txt
```

3️⃣ Download Whisper Model

By default, the scripts use the "base" Whisper model. You can manually download a model if needed:
```
import whisper
whisper.load_model("base")  # Change "base" to "small", "medium", or "large" if needed
```
Usage

- Convert Video to Subtitles Only
To generate English and Arabic subtitles:
```
$ python video_to_srt.py
```
Enter the folder path containing your videos when prompted.

- Convert Video to Subtitles & Dubbed Audio
To generate subtitles and Arabic dubbing:
```
$ python auto_dubber.py
```
Enter the folder path containing your videos when prompted.

Output <br>
For each video, the script will generate:
- video_name.srt – English subtitles
- video_name_ar.srt – Arabic subtitles
- video_name_dubbed.mp4 – Video with Arabic voice dubbing (only for auto_dubber.py)
  
License
This project is licensed under the MIT License.

Author
👤 Muhammed Galal
