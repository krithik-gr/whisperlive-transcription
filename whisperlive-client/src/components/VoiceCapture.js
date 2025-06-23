import React, { useEffect, useRef, useState } from 'react';
import io from 'socket.io-client';

const VoiceCapture = () => {
  const socketRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const recordedChunksRef = useRef([]);
  const [transcript, setTranscript] = useState('');
  const [isRecording, setIsRecording] = useState(false);

  useEffect(() => {
    console.log('📡 Connecting to proxy server...');
    socketRef.current = io('http://localhost:5050');

    socketRef.current.on('connect', () => {
      console.log('✅ Connected to proxy');
    });

    socketRef.current.on('disconnect', () => {
      console.log('❌ Disconnected from proxy');
    });

    socketRef.current.on('transcription', (text) => {
      console.log('📝 Transcription received:', text);
      setTranscript(text);
    });

    return () => {
      socketRef.current.disconnect();
    };
  }, []);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      recordedChunksRef.current = [];

      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm',
      });

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          recordedChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        const blob = new Blob(recordedChunksRef.current, { type: 'audio/webm' });
        const arrayBuffer = await blob.arrayBuffer();

        socketRef.current.emit('audio_blob', arrayBuffer);
        console.log('📤 Sent audio blob to proxy');
      };

      mediaRecorderRef.current = mediaRecorder;
      mediaRecorder.start();
      setIsRecording(true);
      console.log('⏺️ Recording started');
    } catch (err) {
      console.error('🎤 Microphone access error:', err);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      console.log('⏹️ Recording stopped');
    }
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial' }}>
      <h2>🎙️ WhisperLive Voice Transcription</h2>
      <button
        onClick={isRecording ? stopRecording : startRecording}
        style={{
          padding: '10px 20px',
          backgroundColor: isRecording ? '#d9534f' : '#0275d8',
          color: 'white',
          border: 'none',
          borderRadius: '5px',
          fontSize: '16px',
        }}
      >
        {isRecording ? 'Stop Recording' : 'Start Recording'}
      </button>

      <div
        style={{
          marginTop: '20px',
          padding: '15px',
          background: '#f1f1f1',
          borderRadius: '10px',
          fontSize: '16px',
          minHeight: '60px',
        }}
      >
        {transcript ? `📝 ${transcript}` : '🗣️ Say something...'}
      </div>
    </div>
  );
};

export default VoiceCapture;
