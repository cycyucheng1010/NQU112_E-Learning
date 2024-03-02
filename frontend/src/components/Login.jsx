import React, { useState } from "react";
import axios from 'axios';
import { useNavigate } from 'react-router-dom'; // 導入 useNavigate 鉤子
import { useUser} from '../UserContext'; // 導入 useUser 鉤子


export const Login = (props) => {
    const [email, setEmail] = useState('');
    const [pass, setPass] = useState('');
    const navigate = useNavigate(); // 用於導航
    const { setUser } = useUser(); // 使用 setUser 更新用户信息
    
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://127.0.0.1:8000/api/login/', {
                email: email,
                password: pass,
            });
            console.log(response.data);// 登入成功後的操作，例如導航到首頁
            setUser({ username: response.data.username }); // 假设登录响应中包含用户的名字
            navigate('/'); // 導航到首頁
        } catch (error) {
            let errorMessage = 'Login failed: An unexpected error occurred';
            if (error.response) {
                // 请求已发出，服务器以状态码响应不在 2xx 范围
                switch (error.response.status) {
                    case 400:
                        errorMessage = 'Login failed: Invalid email or password';
                        break;
                    case 401:
                        errorMessage = 'Login failed: Unauthorized. Please check your credentials';
                        break;
                    case 403:
                        errorMessage = 'Login failed: Forbidden. You do not have permission to access this resource';
                        break;
                    case 404:
                        errorMessage = 'Login failed: The requested resource was not found';
                        break;
                    // 可以根据需要添加更多的 case
                    default:
                        // 保留默认错误消息
                        break;
                }
            } else if (error.request) {
                // 请求已发出但没有收到响应
                errorMessage = 'Login failed: No response from server. Please try again later';
            }
            console.error('Login error:', error.response ? error.response.data : 'No response');
            alert(errorMessage);
        }
    };
    

    return (
        <div className="auth-form-container">
            <h2>Login</h2>
            <form className="login-form" onSubmit={handleSubmit}>
                <label htmlFor="email">Email</label>
                <input value={email} onChange={(e) => setEmail(e.target.value)} type="email" placeholder="youremail@gmail.com" id="email" name="email" />
                <label htmlFor="password">Password</label>
                <input value={pass} onChange={(e) => setPass(e.target.value)} type="password" placeholder="********" id="password" name="password" />
                <button type="submit">Log In</button>
            </form>
            <button className="link-btn" onClick={() => props.onFormSwitch('register')}>Don't have an account? Register here.</button>
        </div>
    );
};
export default Login;
