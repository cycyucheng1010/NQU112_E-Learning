import React, { useState, useEffect } from 'react';
import './Exam.css';
import axios from 'axios';

const ExamPage = () => {
  const [questions, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [collapsed, setCollapsed] = useState(false);
  const [selectedOption, setSelectedOption] = useState(null);
  const [confirmedAnswers, setConfirmedAnswers] = useState([]);

  useEffect(() => {
    // 使用 Axios 的 POST 方法
    axios.post('https://b403-120-125-96-109.ngrok-free.app/exam/gsat/', {
      fromexamtype: '學測', // 假設需要傳遞的參數是 fromexamtype 和 fromexamnum
      fromexamnum: '103',
    })
      .then(response => setQuestions(response.data.questions))
      .catch(error => console.error('Error fetching questions:', error));
  }, []);

  //if (questions.length === 0) {
    // 資料還在載入中，你可以加入載入中的畫面或其他處理方式
    //return <div>Loading...</div>;
  //}

  const toggleCollapse = () => {
    setCollapsed(!collapsed);
  };

  const handleNextQuestion = () => {
    setCurrentQuestion(prev => Math.min(prev + 1, questions.length - 1));
    setSelectedOption(null); // 清空所選答案
  };

  const handlePrevQuestion = () => {
    setCurrentQuestion(prev => Math.max(prev - 1, 0));
    setSelectedOption(null); // 清空所選答案
  };

  const handleConfirm = () => {
    const answer = selectedOption || '未作答';
    setConfirmedAnswers(prev => [...prev, { question: currentQuestion, answer }]);
    console.log('Question confirmed:', { question: currentQuestion, answer });
  };

  const handleSubmit = () => {
    // 交卷
    console.log('Exam submitted!', confirmedAnswers);
  };

  const currentQuestionData = questions[currentQuestion] || {};

  return (
    <div>
      <div style={{ float: 'left', width: collapsed ? '50px' : '25%' }}>
        <button onClick={toggleCollapse}>題目</button>
        {!collapsed &&
          questions.map((question, index) => (
            <button key={index} onClick={() => setCurrentQuestion(index)}>
              {index + 1}
            </button>
          ))}
      </div>
      <div style={{ marginLeft: collapsed ? '50px' : '25%', width: '75%' }}>
        <div>
          <h2>{currentQuestionData.title}</h2>
          <p>{currentQuestionData.content}</p>
        </div>
        <div>
          {/* 選擇題選項*/}
          {currentQuestionData.options &&
            currentQuestionData.options.map((option, index) => (
              <div key={index}>
                <input
                  type="radio"
                  name={`question-${currentQuestion}`}
                  value={option}
                  checked={selectedOption === option}
                  onChange={() => setSelectedOption(option)}
                />
                {option}
              </div>
            ))}
        </div>
        <div>
          <button onClick={handlePrevQuestion}>上一題</button>
          <button onClick={handleNextQuestion}>下一題</button>
          <button onClick={handleConfirm}>確認</button>
          <button onClick={handleSubmit}>交卷</button>
        </div>
      </div>
    </div>
  );
};

export default ExamPage;
