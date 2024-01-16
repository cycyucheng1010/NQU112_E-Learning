import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import MicIcon from '@mui/icons-material/Mic';
import StopIcon from '@mui/icons-material/Stop';

const VoiceToText = () => {
  const recordingMediaRecorder = useRef(null);
  const [audioBlob, setAudioBlob] = useState(null);
  const [isRecording, setIsRecording] = useState(false);
  const recordingStartRef = useRef(null);
  const recordingStopRef = useRef(null);

  useEffect(() => {
    // 当录音状态改变时，这个effect会被调用
    if (isRecording) {
      console.log('正在录音...');
      if (recordingStartRef.current) {
        recordingStartRef.current.disabled = true;
      }
      if (recordingStopRef.current) {
        recordingStopRef.current.disabled = false;  // 确保停止按钮被启用
      }
    } else {
      console.log('录音停止。');
      if (recordingStartRef.current) {
        recordingStartRef.current.disabled = false;
      }
      if (recordingStopRef.current) {
        recordingStopRef.current.disabled = true;  // 确保停止按钮被禁用
      }
      if (audioBlob) {
        handleUpload();  // 如果有录音数据，则上传
      }
    }
  }, [isRecording, audioBlob]); // 当isRecording或audioBlob变化时触发
  

  const startRecording = async () => {
    console.log('开始录制');
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia || !window.MediaRecorder) {
      alert('你的浏览器不支持 MediaRecorder');
      return;
    }

    const options = {
      audioBitsPerSecond: 128000,
      mimeType: 'audio/webm',
    };

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream, options);
      recordingMediaRecorder.current = mediaRecorder;

      mediaRecorder.onstart = () => console.log('MediaRecorder started');
      mediaRecorder.onstop = () => console.log('MediaRecorder stopped');

      mediaRecorder.addEventListener('dataavailable', (e) => {
        const audioBlob = new Blob([e.data], { type: 'audio/webm' });
        setAudioBlob(audioBlob);
        console.log('音频数据可用');
      });

      mediaRecorder.start();
      setIsRecording(true);
    } catch (error) {
      console.error('获取音频流失败:', error);
    }
  };

  const stopRecording = () => {
    console.log('尝试结束录制');
    if (recordingMediaRecorder.current) {
      recordingMediaRecorder.current.stop();
      setIsRecording(false);
      recordingMediaRecorder.current = null; // Reset the recorder
    } else {
      console.error('没有初始化的MediaRecorder实例');
    }
  };

  const handleUpload = () => {
    if (!audioBlob) {
      console.error('没有音频数据');
      return;
    }

    const formData = new FormData();
    formData.append('file', audioBlob, 'recording.webm');

    let url = "http://localhost:8000/search/VoiceToText/";

    axios.post(url, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }).then(res => {
      console.log('上传成功', res);
      setAudioBlob(null);
    }).catch(error => {
      console.error('上传失败', error);
    });
  };

  return (
    <div>
      {isRecording ? (
        <button onClick={stopRecording} ref={recordingStopRef} disabled={!isRecording}>
          <StopIcon />
        </button>
      ) : (
        <button onClick={startRecording} ref={recordingStartRef} disabled={isRecording}>
          <MicIcon />
        </button>
      )}
    </div>
  );
};

export default VoiceToText;
