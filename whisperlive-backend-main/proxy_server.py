import socketio
import os
import uuid
import eventlet
import eventlet.wsgi

# Socket.IO server for frontend
sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

# Socket.IO client to talk to backend
client_sio = socketio.Client()

@client_sio.event
def connect():
    print("✅ Connected to Whisper backend server at http://localhost:5000")

@client_sio.event
def disconnect():
    print("❌ Disconnected from Whisper backend server.")

@client_sio.on("transcription")
def on_transcription(data):
    print(f"📨 Received transcription from backend: {data}")
    for sid in sio.manager.get_participants("/", None):
        sio.emit("transcription", data, to=sid)

# Connect to backend Whisper server
client_sio.connect("http://localhost:5000")

@sio.event
def connect(sid, environ):
    print(f"[Frontend] ✅ Connected: {sid}")

@sio.event
def disconnect(sid):
    print(f"[Frontend] ❌ Disconnected: {sid}")

@sio.event
def audio_blob(sid, data):
    print(f"🎧 Received audio blob from frontend: {len(data)} bytes")
    try:
        # Save audio to a temp file
        temp_filename = f"temp_{uuid.uuid4().hex}.webm"
        with open(temp_filename, "wb") as f:
            f.write(data)
        print(f"📁 Saved blob as {temp_filename}")

        # Read it back as bytes
        with open(temp_filename, "rb") as f:
            audio_bytes = f.read()

        # Send to backend for transcription
        print("📤 Sending blob to backend for transcription...")
        client_sio.emit("audio", audio_bytes)

        os.remove(temp_filename)

    except Exception as e:
        print(f"⚠ Error handling blob: {e}")
        sio.emit("transcription", "Transcription failed.", to=sid)

# Start proxy
if __name__ == "__main__":
    print("🚀 Starting proxy server on http://localhost:5050")
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5050)), app)
