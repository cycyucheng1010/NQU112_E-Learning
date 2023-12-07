import React, { useState } from 'react';
import { Form, Input, Button, Checkbox } from 'antd';
import 'antd/dist/antd.css';
import './loginComp.css';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const NormalLoginForm = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const submitHandle = () => {
    if (!username || !password) {
      return;
    }

    let data = { username, password };
    let url = 'http://localhost:8000/user/login/';

    axios.post(url, data, { headers: { 'Content-Type': 'application/json' } })
      .then(res => {
        if (res.status === 200 && res.data.code === 1) {
          alert('登录成功。');
          navigate('/');
        } else {
          console.log(res);
          alert('登录失败：' + res.data.msg);
        }
      });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // 验证等其他处理

    submitHandle();
  };

  const handleChangeUsername = (e) => {
    setUsername(e.target.value);
  };

  const handleChangePwd = (e) => {
    setPassword(e.target.value);
  };

  return (
    <div className='login-div'>
      <div className='loginTitle'>登录</div>
      <Form onSubmit={handleSubmit} className="login-form">
        <Form.Item>
          <Input
            placeholder="Username"
            value={username}
            onChange={handleChangeUsername}
          />
        </Form.Item>
        <Form.Item>
          <Input
            type="password"
            placeholder="Password"
            value={password}
            onChange={handleChangePwd}
          />
        </Form.Item>
        <Form.Item>
          <Checkbox style={{ marginLeft: '13%' }}>记住我</Checkbox>
          <Button type="primary" htmlType="submit" className="login-form-button" style={{ marginLeft: '5%' }}>
            登录
          </Button>
          <a className="login-form-forgot" href="http://www.baidu.com" style={{ marginLeft: '5%' }}>
            忘记密码
          </a>
          <a href="/register" style={{ marginLeft: '5%' }}>去注册</a>
        </Form.Item>
      </Form>
    </div>
  );
};

export default NormalLoginForm;
