import React, { useState, useEffect } from "react";
import { useLocation } from 'react-router-dom';
import axios from 'axios';

const ExamPage = () => {
  const location = useLocation();
  const [examData, setExamData] = useState(location.state?.examData || []);
  const [fromexamtype, setFromExamType] = useState(location.state?.fromexamtype || '');
  const [fromexamnum, setFromExamNum] = useState(location.state?.fromexamnum || '');
  const [loading, setLoading] = useState(true);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [selectedQuestion, setSelectedQuestion] = useState(null);
  const [selectedAnswer, setSelectedAnswer] = useState(null);

  const handleDropdownToggle = () => {
    setIsDropdownOpen(!isDropdownOpen);
  };

  const handleSelectQuestion = (questionIndex) => {
    setSelectedQuestion(questionIndex);
    setSelectedAnswer(null);  // 清空已選答案
  };

  const handlePreviousQuestion = () => {
    if (selectedQuestion > 0) {
      setSelectedQuestion(selectedQuestion - 1);
      setSelectedAnswer(null);  // 清空已選答案
    }
  };

  const handleNextQuestion = () => {
    if (selectedQuestion < examData.list5.length - 1) {
      setSelectedQuestion(selectedQuestion + 1);
      setSelectedAnswer(null);  // 清空已選答案
    }
  };

  const handleConfirmAnswer = () => {
    // 使用 selectedAnswer 來獲取所選的答案值
    console.log("Confirmed Answer:", selectedAnswer);
    // 其他處理邏輯...
  };

  const handleSubmitExam = () => {
    // TODO: 實現交卷的邏輯
    console.log("Exam Submitted");
  };

  useEffect(() => {
    if (location.state?.examData) {
      setLoading(false);
      return;
    }

    axios.post('http://127.0.0.1:8000/exam/gsat/', { fromexamtype, fromexamnum }, { headers: { 'Content-Type': 'application/json' } })
      .then(response => {
        console.log('Response data:', response.data);
        setExamData(response.data || []);  // 如果 response.data 不存在，設置為空列表
        setLoading(false);
      })
      .catch(error => {
        console.error('获取考卷数据失败:', error);
        setLoading(false);
      });
  }, [location.state?.examData, fromexamtype, fromexamnum]);

  if (loading) {
    return <div>正在加载考卷数据...</div>;
  }

  return (
    <div style={{ display: 'flex' }}>
      {/* 左邊四分之一，顯示題號 */}
      <div style={{ flex: '1', textAlign: 'center', paddingTop: '50px' }}>
        <button
          style={{ position: 'absolute', left: '10px', top: '70px' }}
          onClick={handleDropdownToggle}
        >
          {isDropdownOpen ? "收起題目" : "題目"}
        </button>

        {isDropdownOpen && (
          <div>
            <h4>選擇題號：</h4>
            <div>
              {examData.list5.map((item, index) => (
                <button
                  key={index}
                  onClick={() => handleSelectQuestion(index)}
                >
                  {index + 1}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* 右邊上半部，顯示題目內容 */}
      <div style={{ flex: '3', textAlign: 'center', paddingTop: '50px' }}>
        {selectedQuestion !== null && (
          <div>
            <h4>第 {selectedQuestion + 1} 題：</h4>
            <p>{examData.list5[selectedQuestion]}</p>
          </div>
        )}
      </div>

      {/* 右邊下半部，顯示選項、上一題、下一題、確認按鈕和交卷按鈕 */}
      <div style={{ flex: '3', textAlign: 'center', paddingTop: '50px' }}>
  {selectedQuestion !== null && (
    <div>
      <h4>選項：</h4>
      <div>
        {examData?.list1 && (
          <button onClick={() => setSelectedAnswer(examData.list1[selectedQuestion])}>
            {examData.list1[selectedQuestion]}
          </button>
        )}
        {examData?.list2 && (
          <button onClick={() => setSelectedAnswer(examData.list2[selectedQuestion])}>
            {examData.list2[selectedQuestion]}
          </button>
        )}
        {examData?.list3 && (
          <button onClick={() => setSelectedAnswer(examData.list3[selectedQuestion])}>
            {examData.list3[selectedQuestion]}
          </button>
        )}
        {examData?.list4 && (
          <button onClick={() => setSelectedAnswer(examData.list4[selectedQuestion])}>
            {examData.list4[selectedQuestion]}
          </button>
        )}
        {/* 以此類推，檢查每一個 list */}
      </div>
          </div>
        )}

        {/* 上一題、下一題按鈕 */}
        <div>
          <button onClick={handlePreviousQuestion} disabled={selectedQuestion === 0}>
            上一題
          </button>
          <button onClick={handleNextQuestion} disabled={selectedQuestion === examData.list5.length - 1}>
            下一題
          </button>
        </div>

        {/* 確認答案按鈕 */}
        <div>
          <button onClick={handleConfirmAnswer}>確認答案</button>
        </div>

        {/* 交卷按鈕 */}
        <div>
          <button onClick={handleSubmitExam}>交卷</button>
        </div>
      </div>
    </div>
  );
};

export default ExamPage;
