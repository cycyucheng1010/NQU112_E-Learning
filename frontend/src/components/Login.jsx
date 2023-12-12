import React, { useState } from "react";
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

export const Login = (props) => {
    const [email, setEmail] = useState('');
    const [password, setPass] = useState('');
    const navigate = useNavigate();
    
    const submitHandle = () => {
        if (!email || !password) {
          return;
        }
    
        let data = { email, password };
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
        submitHandle();
        console.log(email);
    }

    return (
        <div className="auth-form-container">
            <h2>Login</h2>
            <form className="login-form" onSubmit={handleSubmit}>
                <label htmlFor="email">email</label>
                <input value={email} onChange={(e) => setEmail(e.target.value)}type="email" placeholder="youremail@gmail.com" id="email" name="email" />
                <label htmlFor="password">password</label>
                <input value={password} onChange={(e) => setPass(e.target.value)} type="password" placeholder="********" id="password" name="password" />
                <button type="submit">Log In</button>
            </form>
            <button className="link-btn" onClick={() =>navigate('/register') }>Don't have an account? Register here.</button>
        </div>
    )
}

export default Login