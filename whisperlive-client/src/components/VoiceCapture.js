import React, { useEffect, useRef, useState } from 'react';
import io from 'socket.io-client';

const VoiceCapture = () => {
  const socketRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const recordedChunksRef = useRef([]);
  const [transcript, setTranscript] = useState('');
  const [isRecording, setIsRecording] = useState(false);

  // Connect socket on mount
  useEffect(() => {
    console.log('📡 Connecting to socket...');
    socketRef.current = io('http://localhost:6000');

    socketRef.current.on('connect', () => {
      console.log('✅ Connected to proxy server');
    });

    socketRef.current.on('disconnect', () => {
      console.log('⚠️ Disconnected from socket');
    });

    socketRef.current.on('transcription', (text) => {
      console.log('📝 Transcription:', text);
      setTranscript(text);
    });

    return () => {
      socketRef.current.disconnect();
    };
  }, []);

  // Start recording
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      recordedChunksRef.current = [];

      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm'
      });

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          recordedChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(recordedChunksRef.current, { type: 'audio/webm' });
        socketRef.current.emit('audio_blob', audioBlob);
        console.log('📤 Audio blob sent');
      };

      mediaRecorderRef.current = mediaRecorder;
      mediaRecorder.start();
      setIsRecording(true);
      console.log('⏺️ Recording started');
    } catch (err) {
      console.error('🎤 Microphone access denied:', err);
    }
  };

  // Stop recording
  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      console.log('⏹️ Recording stopped');
    }
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial' }}>
      <h2>🎙️ WhisperLive Transcription</h2>
      <button onClick={isRecording ? stopRecording : startRecording}>
        {isRecording ? 'Stop Recording' : 'Start Recording'}
      </button>
      <div
        style={{
          marginTop: '20px',
          padding: '10px',
          background: '#f5f5f5',
          borderRadius: '8px',
          fontSize: '16px'
        }}
      >
        {transcript || '🔊 Speak something...'}
      </div>
    </div>
  );
};

export default VoiceCapture;
