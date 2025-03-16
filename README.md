# video-subtitle-converter
This script extracts audio from video files, transcribes it into text using OpenAI's Whisper, generates an SRT subtitle file, and translates it into Arabic.

🔹 Features
✅ Convert video to subtitles (.srt)
✅ Transcribe audio using Whisper (local model, no API required)
✅ Translate subtitles from English to Arabic
✅ Supports multiple video formats: .mp4, .avi, .mov, .mkv

⚡ Installation
1️⃣ Clone the Repository:
```
git clone https://github.com/Dg0x6/video-subtitle-converter.git
cd video-subtitle-converter
```
2️⃣ Install Dependencies
Make sure you have Python installed (Python 3.8+ recommended). Then, run:
```
pip install -r requirements.txt
```
3️⃣ Download Whisper Model
The script uses the base model by default. You can change it to small, medium, or large.
To manually download a model:
```
import whisper
whisper.load_model("base")  # Change "base" to another model if needed
```

🚀 Usage
Run the script:
```
python video_subtitle_converter.py
Enter the folder path containing your videos when prompted.
```

🎯 Output
For each video, the script will generate:

Original subtitles: video_name.srt
Translated subtitles (Arabic): video_name.translated.srt
📜 License
This project is licensed under the MIT License.

💡 Author
👤 Muhammed Galal
