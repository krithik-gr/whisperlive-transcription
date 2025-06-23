from faster_whisper import WhisperModel
import sys
import os

# Load the Whisper model
model = WhisperModel("base", compute_type="float32")

def transcribe_audio(file_path):
    if not os.path.isfile(file_path):
        print(f"❌ File not found: {file_path}")
        return

    print(f"🔍 Transcribing: {file_path}")
    segments, _ = model.transcribe(file_path)

    full_text = " ".join([segment.text for segment in segments])
    print("📝 Transcription:\n")
    print(full_text.strip())

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python transcribe_file.py <audio_file_path>")
    else:
        transcribe_audio(sys.argv[1])
