import React, { useState, useRef, useLayoutEffect, useMemo } from 'react';
import './Exam.css'; // 引入自定義的 CSS 文件

function Exam() {
  const [selectedOption, setSelectedOption] = useState('');
  const [drawerOpen, setDrawerOpen] = useState(false);
  const buttonData = ["按钮1", "按钮2", "按钮3", "按钮4", "按钮5"];
  const [pHeight, setPHeight] = useState('auto');
  const [divHeight, setDivHeight] = useState('500px');
  const examQuestions = ['如何看待气候变化对社会和环境的影响？'];
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [examAnswers, setExamAnswers] = useState([]); // 保存答案的狀態

  const handleOptionChange = (e) => {
    setSelectedOption(e.target.value);
  };
  const pRef = useRef(null);
  const divRef = useRef(null);

  const handlePrevQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
    }
  };

  const handleNextQuestion = () => {
    if (currentQuestionIndex < examQuestions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    }
  };

  const handleSubmitExam = () => {
    // 這裡可以處理提交考卷的邏輯，例如將答案發送到後端
    // 這裡只是將答案打印到控制台上作為示例
    console.log('提交的答案:', examAnswers);
  };



  useLayoutEffect(() => {
    if (pRef.current.scrollHeight > pRef.current.parentElement.clientHeight) {
      setPHeight(`${pRef.current.scrollHeight}px`);

      // 只有在 <p> 內容超出時才動態調整 <div> 的高度
      if (divRef.current.clientHeight < pRef.current.scrollHeight) {
        setDivHeight(`${pRef.current.scrollHeight}px`);
      }
    }
  }, [examQuestions]);

  

  return (
    <div className="exam-container">
      <div ref={divRef} className="topic" style={{ height: divHeight, overflow: 'visible' }}>
        <h2>Question</h2>
        <p ref={pRef}>{examQuestions}</p>
      </div>
      
      <div className={`button-container ${drawerOpen ? 'open' : ''}`}>
      <h1>第一大題</h1>
      {buttonData.map((item, index) => (
      <button key={index} className="myButton" onClick={() => alert(`按钮 ${item} 被点击`)}>
      {`${index + 1}`}
     </button>
       ))}
       <h1>第二大題</h1>
      {buttonData.map((item, index) => (
      <button key={index} className="myButton" onClick={() => alert(`按钮 ${item} 被点击`)}>
      {`${index + 1}`}
     </button>
       ))}
       <h1>第三大題</h1>
      {buttonData.map((item, index) => (
      <button key={index} className="myButton" onClick={() => alert(`按钮 ${item} 被点击`)}>
      {`${index + 1}`}
     </button>
       ))}
       <h1>第四大題</h1>
      {buttonData.map((item, index) => (
      <button key={index} className="myButton" onClick={() => alert(`按钮 ${item} 被点击`)}>
      {`${index + 1}`}
     </button>
       ))}
       <h1>第五大題</h1>
      {buttonData.map((item, index) => (
      <button key={index} className="myButton" onClick={() => alert(`按钮 ${item} 被点击`)}>
      {`${index + 1}`}
     </button>
       ))}
      </div>

      <div className='select'>
        <h2>选择题</h2>

        <form>
          <label>
            <input
              type="radio"
              value="option1"
              checked={selectedOption === 'option1'}
              onChange={handleOptionChange}
            />
            选项1
          </label>

          <label>
            <input
              type="radio"
              value="option2"
              checked={selectedOption === 'option2'}
              onChange={handleOptionChange}
            />
            选项2
          </label>

          <label>
            <input
              type="radio"
              value="option3"
              checked={selectedOption === 'option3'}
              onChange={handleOptionChange}
            />
            选项3
          </label>

          <label>
            <input
              type="radio"
              value="option"
              checked={selectedOption === 'option4'}
              onChange={handleOptionChange}
            />
            选项4
          </label>
        </form>

        {selectedOption && (
          <div>
            <h3>你选择的选项是: {selectedOption}</h3>
          </div>
        )}
      </div>

      <div className='next'>
      <button onClick={handlePrevQuestion} disabled={currentQuestionIndex === 0}>
          上一题
        </button>

        <button onClick={handleNextQuestion} disabled={currentQuestionIndex === examQuestions.length - 1}>
          下一题
        </button>

        <button onClick={handleSubmitExam}>
          提交考卷
        </button>
      </div>
    </div>
  );
}

export default Exam;
