import React, { useState } from "react";
import { Form, Button } from "react-bootstrap";
import "./SelectExam.css";
import axios from 'axios';
import { useNavigate } from 'react-router-dom';


function SelectExam() {
  const [fromexamtype, setexamtype] = useState("");
  const [fromexamnum, setexamnum] = useState([]);

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
  setexamtype(examtype.name);
  setexamnum(examtype.examnum);
} else {
  // 在這裡處理找不到匹配的情況
  console.error("找不到匹配的考卷類型");
}
  };

  const handleExamNumChange = (e) => {
  };

  const handleSubmit = () => {
    if (!fromexamtype||!fromexamnum ) {
      return;
    }
    let data = {  fromexamtype, fromexamnum };
    console.log("提交的数据：", data); // 打印数据到控制台

    let url = 'http://localhost:8000/user/register/';
    axios.post(url, data, { headers: { 'Content-Type': 'application/json' } })
  };

  return (
    <div className="contain">
      <Form.Group controlId="custom-select" className="sec-center">
        {/* 考卷下拉選單 */}
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
        {/* 考卷編號下拉選單 */}
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
              <option key={key} title="" value={num}>
                {num}
              </option>
            ))}
          </Form.Control>
        </div>
        {/* 提交按钮 */}
        <div className="contain2">
          <Button variant="primary" onClick={handleSubmit}>
            提交
          </Button>
        </div>
      </Form.Group>
    </div>
  );
}

export default SelectExam;
