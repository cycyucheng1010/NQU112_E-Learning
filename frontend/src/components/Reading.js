import React, { useState } from "react";
import axios from 'axios';

const ReadingComponent = () => {
  const [article, setArticle] = useState('');
  const [questions, setQuestions] = useState('');
  const [answer, setAnswer] = useState('');
  const [articleButtonPressed, setArticleButtonPressed] = useState(false);
  const [answerButtonPressed, setAnswerButtonPressed] = useState(false);
  const [answerComparison, setAnswerComparison] = useState([]);

  const formatText = (text) => {
    if (!text) return text;
    return text.split('\n\n').map((paragraph, index) => (
      <p key={index}>{paragraph}</p>
    ));
  };

  const createDropdowns = (text) => {
    if (!text) return text;
    return text.split('\n\n').map((paragraph, index) => {
      const match = paragraph.match(/(\d+)/);
      if (match && (match[1] === '1' || match[1] === '2' || match[1] === '3')) {
        return (
          <div key={index}>
            <label htmlFor={`question${match[1]}`}></label>
            <select id={`question${match[1]}`} name={`question${match[1]}`} style={{ color: answerComparison[index] || 'black' }}>
              <option value="...">...</option>
              <option value="A">A</option>
              <option value="B">B</option>
              <option value="C">C</option>
              <option value="D">D</option>
            </select>
            {paragraph}
          </div>
        );
      } else {
        return <p key={index}>{paragraph}</p>;
      }
    });
  };

  const fetchArticleAndQuestions = async () => {
    try {
      const { data } = await axios.post('http://127.0.0.1:8000/reading/reading_question/', {
        message_type: 'article',
      });
      setArticle(formatText(data.response));

      const { data: questionData } = await axios.post('http://127.0.0.1:8000/reading/reading_question/', {
        message_type: 'question',
      });
      setQuestions(createDropdowns(questionData.response));
    } catch (error) {
      console.error('Error generating article and questions:', error);
    } finally {
      setArticleButtonPressed(false);
    }
  };

  const fetchAnswer = async () => {
    try {
      const selectedValues = Array.from(document.querySelectorAll('select')).map(select => select.value).join(',');

      const { data: answerData } = await axios.post('http://127.0.0.1:8000/reading/reading_question/', {
        message_type: 'answer',
        selected_values: selectedValues,
      });
      setAnswer(formatText(answerData.response));

      const { data: answerAnswerData } = await axios.post('http://127.0.0.1:8000/ReadingAnswer/reading_answer/', {
        message_type: 'correctanswer',
        user_answer: selectedValues,
        gpt_answer: answerData.response,
      });

      // 设置每个选项的字体颜色
      const colors = answerAnswerData.comparison_result.map(result => result === 0 ? 'green' : 'red');
      setAnswerComparison(colors);
    } catch (error) {
      console.error('Error generating answer:', error);
    } finally {
      setAnswerButtonPressed(false);
    }
  };

  const handleArticleAndQuestionsButtonClick = async () => {
    setArticleButtonPressed(true);
    await fetchArticleAndQuestions();
  };

  const handleAnswerButtonClick = async () => {
    setAnswerButtonPressed(true);
    await fetchAnswer();
  };

  return (
    <div>
      <button onClick={handleArticleAndQuestionsButtonClick} disabled={articleButtonPressed || answerButtonPressed} style={{ 
        backgroundImage: 'linear-gradient(to right, #BA55D3, #FFD700,  #BA55D3)', 
        color: 'black',
        border: articleButtonPressed ? '2px solid #FFFFFF' : '2px solid  #808080',
        padding: '10px 20px',
        borderRadius: '5px',
        cursor: 'pointer'
      }}>Generate Article and Questions</button>

      <button onClick={handleAnswerButtonClick} disabled={answerButtonPressed || !article || !questions} style={{ 
        backgroundImage: 'linear-gradient(to right, #BA55D3, #FFD700,  #BA55D3)', 
        color: 'black',
        border: answerButtonPressed ? '2px solid #FFFFFF' : '2px solid  #808080',
        padding: '10px 20px',
        borderRadius: '5px',
        cursor: 'pointer',
        marginLeft: '20px'
      }}>Generate Answer</button>

      <div>
        <h3>Article:</h3>
        <div className="card" style={{ textAlign: 'left', lineHeight: '1.6', fontFamily: 'Arial, sans-serif' }}>{article}</div>
      </div>
      
      <div>
        <h3>Questions:</h3>
        <div style={{ textAlign: 'left', lineHeight: '1.6', fontFamily: 'Arial, sans-serif' }}>{questions}</div>
      </div>

      {answer && (
        <div>
          <h3>Answer:</h3>
          <div style={{ textAlign: 'left', lineHeight: '1.6', fontFamily: 'Arial, sans-serif' }}>
            {answer.map((paragraph, index) => (
              <p key={index} style={{ color: answerComparison[index] }}>{paragraph}</p>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ReadingComponent;