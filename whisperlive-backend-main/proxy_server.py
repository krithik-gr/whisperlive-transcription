import socketio
from werkzeug.serving import run_simple

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)
client_sio = socketio.Client()

@sio.event
def connect(sid, environ):
    print(f"[Frontend] Connected: {sid}")

@sio.event
def disconnect(sid):
    print(f"[Frontend] Disconnected: {sid}")

@sio.event
def audio_blob(sid, data):
    print(f"📨 Received audio blob from frontend: {len(data)} bytes")
    if client_sio.connected:
        client_sio.emit("audio_blob", data)

@client_sio.event
def transcription(data):
    print(f"[🎤 Backend] Transcription: {data}")
    sio.emit("transcription", data)

def start_whisperlive_client():
    try:
        print("🔌 Connecting to WhisperLive at http://localhost:5000...")
        client_sio.connect("http://localhost:5000")
        print("✅ Connected to WhisperLive!")
    except Exception as e:
        print(f"❌ Could not connect to WhisperLive: {e}")

if __name__ == '__main__':
    start_whisperlive_client()
    print("🚀 Starting proxy server on port 6000...")
    run_simple('0.0.0.0', 6000, app)