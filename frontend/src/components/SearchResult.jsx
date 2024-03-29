import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import MicIcon from '@mui/icons-material/Mic';
import StopIcon from '@mui/icons-material/Stop';

function SearchResult() {
  const [displayWord, setDisplayWord] = useState('');
  const [audioBlob, setAudioBlob] = useState(null);
  const [isRecording, setIsRecording] = useState(false);
  const [matchResult, setMatchResult] = useState(null);  // 用于存储比对结果
  const recordingMediaRecorder = useRef(null);
  const [imageURL, setImageURL] = useState(''); // 存储图像URL的状态
  const [displaySentence, setDisplaySentence] = useState('');

  useEffect(() => {
    // 指定后端API地址
    const url = `http://localhost:8000/result/sentence/`; // 更改为匹配您的后端API的URL

    axios.post(url, { word: displayWord })  // 确保发送单词到后端
      .then(response => {
        if (response.data.msg === 'success') {
          // 更新状态以显示句子和图片
          setDisplaySentence(response.data.existing_sentence || response.data.generated_sentence);
          setImageURL(response.data.existing_image || response.data.generated_image_url);
        } else {
          console.error('Error: ' + response.data.error_details);
        }
      })
      .catch(error => {
        console.error("Error fetching the data: ", error);
      });
  }, [displayWord]); // 当displayWord变化时重新运行

  useEffect(() => {
    // 指定后端API地址

    const url = `http://localhost:8000/result/get_last_word/`;
    
    axios.get(url)
      .then(response => {
        if (response.data.status === 'success') {
          setDisplayWord(response.data.word);
        } else {
          console.error('Error: ' + response.data.message);
        }
      })
      .catch(error => {
        console.error("Error fetching the data: ", error);
      });
  }, []);

  const startRecording = async () => {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia || !window.MediaRecorder) {
      alert('你的浏览器不支持 MediaRecorder');
      return;
    }
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      recordingMediaRecorder.current = mediaRecorder;

      mediaRecorder.onstart = () => console.log('MediaRecorder started');
      mediaRecorder.onstop = () => console.log('MediaRecorder stopped');

      mediaRecorder.addEventListener('dataavailable', (e) => {
        setAudioBlob(new Blob([e.data], { type: 'audio/webm' }));
      });

      mediaRecorder.start();
      setIsRecording(true);
    } catch (error) {
      console.error('获取音频流失败:', error);
    }
  };

  const stopRecording = () => {
    if (recordingMediaRecorder.current) {
      recordingMediaRecorder.current.stop();
      setIsRecording(false);
      recordingMediaRecorder.current = null;
    } else {
      console.error('没有初始化的MediaRecorder实例');
    }
  };

  const handleUpload = () => {
    if (!audioBlob || !displayWord) {
      console.error('没有音频数据或单词');
      return;
    }

    const formData = new FormData();
    formData.append('file', audioBlob);
    formData.append('word', displayWord);

    let url = "http://localhost:8000/result/compare_word/";
    axios.post(url, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    .then(res => {
      console.log('上传成功', res);
      if (res.data.status === 'success') {
        // 处理比对结果
        setMatchResult(res.data.match ? '匹配' : '不匹配');
      } else {
        alert('Error: ' + res.data.message);
      }
    })
    .catch(error => {
      console.error('上传失败', error);
    });
  };

  useEffect(() => {
    if (!isRecording && audioBlob) {
      handleUpload();  // 如果有录音数据，则上传
    }
  }, [isRecording, audioBlob]);
  const wordLink = `https://dictionary.cambridge.org/dictionary/english-chinese-traditional/${displayWord}`;
  return (
    <div>
        <div style={{ display: 'flex', alignItems: 'center' }}>
            {/* 先显示单词，然后是麦克风 */}
            
            <a href = {wordLink}>
            <h1 style={{ marginRight: '10px' }}> Word: {displayWord}</h1>
            </a>
            {isRecording ? (
                <button onClick={stopRecording}>
                    <StopIcon />
                </button>
            ) : (
                <button onClick={startRecording}>
                    <MicIcon />
                </button>
            )}
        </div>
        <div>
            {/* 显示生成的句子 */}
            <p>例句: {displaySentence}</p>
        </div>
        <div>
            {/* 显示图像 */}
            {imageURL && <img src={imageURL} alt="Generated" />}
        </div>
        {matchResult && <p>比对结果: {matchResult}</p>}
    </div>
);
}

export default SearchResult;

