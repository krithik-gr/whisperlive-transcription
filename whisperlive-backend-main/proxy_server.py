import socketio
import tempfile
import os
import uuid
import eventlet
import eventlet.wsgi

# Socket.IO server (Frontend <-> Proxy)
sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

# Socket.IO client (Proxy <-> Backend)
client_sio = socketio.Client()

# Connect to the backend Whisper server (run_server.py)
@client_sio.event
def connect():
    print("✅ Connected to Whisper backend server at http://localhost:5000")

@client_sio.event
def disconnect():
    print("❌ Disconnected from Whisper backend server.")

@client_sio.on("transcription")
def on_transcription(data):
    print(f"📨 Received transcription from backend: {data}")
    
    # ✅ Broadcast transcription to all connected frontend clients
    for sid in list(sio.manager.rooms["/"]):
        print(f"📢 Emitting transcription to frontend: {sid}")
        sio.emit("transcription", data, to=sid)

# Connect to backend server
client_sio.connect("http://localhost:5000")


# === FRONTEND EVENTS ===

@sio.event
def connect(sid, environ):
    print(f"[Frontend] ✅ Connected: {sid}")
    # Optional test message
    # sio.emit("transcription", "📢 Hello from proxy!", to=sid)

@sio.event
def disconnect(sid):
    print(f"[Frontend] ❌ Disconnected: {sid}")

@sio.event
def audio_blob(sid, data):
    print(f"🎧 Received audio blob from frontend: {len(data)} bytes")

    try:
        # Save to temp file
        temp_filename = f"temp_{uuid.uuid4().hex}.webm"
        with open(temp_filename, "wb") as f:
            f.write(data)
        print(f"📁 Saved blob as {temp_filename}")

        # Read and forward to backend
        with open(temp_filename, "rb") as f:
            audio_bytes = f.read()

        print("📤 Sending blob to backend for transcription...")
        client_sio.emit("audio", audio_bytes)

        os.remove(temp_filename)

    except Exception as e:
        print(f"⚠ Error handling blob: {e}")
        sio.emit("transcription", "Transcription failed.", to=sid)


# ✅ Start proxy server
if __name__ == '__main__':
    print("🚀 Starting proxy server on http://localhost:5050")
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5050)), app)
