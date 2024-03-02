import React, { useState } from "react";
import axios from 'axios';
import { useNavigate } from 'react-router-dom'; // 導入 useNavigate 
import "../App.css";
export const Register = (props) => {
    const [email, setEmail] = useState('');
    const [pass, setPass] = useState('');
    const [name, setName] = useState('');
    const navigate = useNavigate(); // 用於導航

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://127.0.0.1:8000/api/register/', {
                email: email,
                password: pass,
                username: name,
            });
            console.log(response.data);
            alert('registration success');
            // 註冊成功後的操作，例如導航到登入頁面
            navigate('/auth'); // 假設 '/auth' 是登入頁面的路徑
        } catch (error) {
            console.error('Registration failed:', error.response ? error.response.data : 'No response');
            alert('Registration failed');
        }
    };

    return (
        <div className="auth-form-container">
            <h2>Register</h2>
            <form className="register-form" onSubmit={handleSubmit}>
                <label htmlFor="name">Full Name</label>
                <input value={name} onChange={(e) => setName(e.target.value)} id="name" placeholder="Full Name" />
                <label htmlFor="email">Email</label>
                <input value={email} onChange={(e) => setEmail(e.target.value)} type="email" placeholder="youremail@gmail.com" id="email" name="email" />
                <label htmlFor="password">Password</label>
                <input value={pass} onChange={(e) => setPass(e.target.value)} type="password" placeholder="********" id="password" name="password" />
                <button type="submit">Register</button>
            </form>
            <button className="link-btn" onClick={() => props.onFormSwitch('login')}>Already have an account? Login here.</button>
        </div>
    );
};
export default Register;