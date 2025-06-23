# 🎙️ WhisperLive – Real-Time Voice Transcription System

This is a complete setup guide for the **WhisperLive** project, which enables real-time voice transcription using a React frontend, a proxy server, and a Python backend with [faster-whisper](https://github.com/guillaumekln/faster-whisper).

---

## 📁 Folder Structure

whisperlive-backend-main/
├── whisperlive-client/ ← React frontend
│ ├── public/
│ ├── src/
│ │ ├── components/
│ │ │ └── VoiceCapture.js
│ │ ├── App.js
│ │ └── index.js
│ ├── package.json
│ └── ...
├── run_server.py ← Main Whisper backend
├── proxy_server.py ← Proxy between frontend and backend
├── requirements.txt
├── README.md or FULL_SETUP_GUIDE.md ← This file

cd whisperlive-client
npm install
npm install socket.io-client react-scripts
npm start
