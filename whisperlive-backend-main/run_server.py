import socketio
import tempfile
import os
from faster_whisper import WhisperModel

# Initialize socket server
sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

# Load model once (you can change "base" to "small", "medium", "large")
print("⏳ Loading Whisper model...")
model = WhisperModel("base", compute_type="float32")  # or "int8" for faster/slower GPUs
print("✅ Whisper model loaded and ready!")

@sio.event
def connect(sid, environ):
    print(f"[Proxy] ✅ Connected: {sid}")

@sio.event
def disconnect(sid):
    print(f"[Proxy] ❌ Disconnected: {sid}")

@sio.on("audio")
def handle_audio(sid, data):
    try:
        with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as tmp:
            tmp.write(data)
            tmp_path = tmp.name

        print(f"🔍 Received audio file: {tmp_path}")
        print("📦 Size:", os.path.getsize(tmp_path), "bytes")

        # Transcribe the file
        segments, _ = model.transcribe(tmp_path)
        result = " ".join([segment.text for segment in segments])
        print(f"📝 Transcription result: {result.strip()}")

        # Emit back to proxy
        sio.emit("transcription", result.strip())

        # Cleanup
        os.remove(tmp_path)

    except Exception as e:
        print("❌ Error during transcription:", e)
        sio.emit("transcription", "Transcription failed.")

# Start backend
if __name__ == "__main__":
    import eventlet
    print("🚀 Starting backend server on http://localhost:5000")
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)
