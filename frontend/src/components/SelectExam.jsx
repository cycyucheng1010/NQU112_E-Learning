import React, { useState, useEffect } from "react";
import { Form, Button } from "react-bootstrap";
import "./SelectExam.css";
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function SelectExam() {
  const navigate = useNavigate();
  const [selectedExamNum, setSelectedExamNum] = useState('');
  const [fromexamtype, setExamType] = useState("");
  const [fromexamnum, setExamNum] = useState([]);
  const [screenWidth, setScreenWidth] = useState(window.innerWidth);

  const handleWindowResize = () => {
    setScreenWidth(window.innerWidth);
  };

  useEffect(() => {
    window.addEventListener("resize", handleWindowResize);
    return () => {
      window.removeEventListener("resize", handleWindowResize);
    };
  }, []);

  const ExamList = [
    {
      name: '學測',
      code: 'T1',
      examnum: ["112", "111", "110", "109", "108", "107", "106", "105", "104", "103"]
    },
    {
      name: '全民英檢',
      code: 'T2',
      examnum: ["高級", "中級", "初級"]
    }
  ];

  const handleFromCountries = (e) => {
    const examtype = ExamList.find((exam) => exam.name === e.target.value);

    if (examtype) {
      setExamType(examtype.name);
      setExamNum(examtype.examnum);
    } else {
      console.error("找不到匹配的考卷類型");
    }
  };

  const handleExamNumChange = (e) => {
    const selectedNum = e.target.value;
    setSelectedExamNum(selectedNum);
  };

  const handleSubmit = () => {
    if (!fromexamtype || selectedExamNum.length === 0) {
      console.error('请选择考卷类型和编号');
      return;
    }

    let data = { fromexamtype, fromexamnum: selectedExamNum };
    console.log('提交的数据：', data);

    let url = 'http://127.0.0.1:8000/exam/gsat/';
    axios.post(url, data, { headers: { 'Content-Type': 'application/json' } })
      .then(response => {
        console.log('成功提交:', response.data);

        // 使用新的导航方式，传递参数
        navigate('/exam', { state: { examData: response.data, fromexamtype, fromexamnum } });
      })
      .catch(error => {
        console.error('提交失败:', error);
      });
  };

  return (
    <div>
      <div className="slogan">
        {screenWidth > 768 ? (
          <>
            <p>選擇你的考試，開始挑戰！</p>
          </>
        ) : (
          <>
            <p>選擇你的考試，</p>
            <p>開始挑戰！</p>
          </>
        )}
      </div>

      <div className="contain">
        <Form.Group controlId="custom-select" className="sec-center">
          <div className="contain2">
            <Form.Label>選擇考卷</Form.Label>
            <Form.Control
              as="select"
              className="rounded-0"
              onChange={(e) => handleFromCountries(e)}
            >
              <option className="d-none" value="">
                選擇考試種類
              </option>
              {ExamList.map((exam, key) => (
                <option key={key} title={exam.code} value={exam.name}>
                  {exam.name}
                </option>
              ))}
            </Form.Control>
          </div>
          <div className="contain2">
            <Form.Label>選擇考卷編號</Form.Label>
            <Form.Control
              as="select"
              className="rounded-0"
              onChange={(e) => handleExamNumChange(e)}
            >
              <option className="d-none" value="">
                選擇考卷編號
              </option>
              {fromexamnum.map((num, key) => (
                <option key={key} value={num}>
                  {num}
                </option>
              ))}
            </Form.Control>
          </div>
          <div className="contain3">
            <Button variant="primary" onClick={handleSubmit}>
              提交
            </Button>
          </div>
        </Form.Group>
      </div>
    </div>
  );
}

export default SelectExam;
