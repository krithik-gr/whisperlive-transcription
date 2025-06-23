import socketio
import eventlet
from faster_whisper import WhisperModel
import numpy as np
import tempfile
import soundfile as sf

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

print("🔄 Loading Whisper model...")
model = WhisperModel("base")
print("✅ Whisper model loaded!")

@sio.event
def connect(sid, environ):
    print(f"🔌 Client connected: {sid}")

@sio.event
def disconnect(sid):
    print(f"❌ Client disconnected: {sid}")

@sio.event
def audio_blob(sid, blob_data):
    print(f"🎵 Received audio blob from {sid} - {len(blob_data)} bytes")
    try:
        with tempfile.NamedTemporaryFile(suffix=".webm", delete=True) as f:
            f.write(blob_data)
            f.flush()
            audio, _ = sf.read(f.name, dtype='float32')

        segments, _ = model.transcribe(audio)
        full_text = " ".join(segment.text for segment in segments).strip()

        if full_text:
            print(f"📝 Transcribed: {full_text}")
            sio.emit("transcription", full_text, to=sid)
        else:
            print("🔇 No speech detected.")
    except Exception as e:
        print(f"⚠️ Error decoding/transcribing blob: {e}")
        sio.emit("transcription", '', to=sid)

if __name__ == '__main__':
    print("🚀 Starting WhisperLive backend on port 5000...")
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)
