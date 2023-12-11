import React, { useState } from "react";
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
export const Register = (props) => {
  const [email, setEmail] = useState('');
  const [password, setPass] = useState('');
  const [username, setName] = useState('');
  const navigate = useNavigate();

  const submitH = () => {
    if (!email || !password || !username) {
      return;
    }
    let data = { email, password, username };
    let url = 'http://localhost:8000/user/register/';
    axios.post(url, data, { headers: { 'Content-Type': 'application/json' } })
      .then(res => {
        if (res.status === 200 && res.data.code === 1) {
          alert('註冊成功。' + res);
          navigate('/login');// 修改此行，移除this.props
        } else {
          console.log(res);
          alert('註冊失敗：' + res.data.msg);
        }
      });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    submitH();
    console.log(email);
  };

  return (
    <div className="auth-form-container">
      <h2>Register</h2>
      <form className="register-form" onSubmit={handleSubmit}>
        <label htmlFor="username">全名</label>
        <input value={username} onChange={(e) => setName(e.target.value)} id="username" placeholder="全名" />
        <label htmlFor="email">電子郵件</label>
        <input value={email} onChange={(e) => setEmail(e.target.value)} type="email" placeholder="youremail@gmail.com" id="email" name="email" />
        <label htmlFor="password">密碼</label>
        <input value={password} onChange={(e) => setPass(e.target.value)} type="password" placeholder="********" id="password" name="password" />
        <button type="submit">註冊</button>
      </form>
      <button className="link-btn" onClick={() => navigate('/login')}>已經有帳號?在此登入。</button>
    </div>
  );
};

export default Register;
