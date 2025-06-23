#  WhisperLive Backend

This is the Python backend for real-time speech-to-text transcription using Whisper.  
It acts as a bridge between a **React frontend** and the **WhisperLive transcription server**, enabling live microphone input from the browser.

---

##  Features

- Real-time transcription using OpenAI's Whisper model
- Socket.IO connection between browser and backend
- Supports easy integration with frontend (React + whisper-live client)

---

## Setup Instructions

```bash
- git clone https://github.com/sanaabdullapk/whisperlive-backend.git
- cd whisperlive-backend
- python -m venv backend-env
- pip install -r requirements.txt
- python run_server.py
- python proxy_server.py


