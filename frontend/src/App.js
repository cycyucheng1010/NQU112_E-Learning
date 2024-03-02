import React, { useContext, useState } from "react";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { useLocation } from 'react-router-dom';
import Navbar from "./components/Navbar/Navbar";
import Intro from "./components/Intro/Intro";
import Services from "./components/Services/Services";
import Experience from "./components/Experience/Experience";
import Works from "./components/Works/Works";
import Portfolio from "./components/Portfolio/Portfolio";
import Testimonial from "./components/Testimonials/Testimonial";
import Contact from "./components/Contact/Contact";
import Footer from "./components/Footer/Footer";
import { Login } from "./components/Login";
import { Register } from "./components/Register";
import { themeContext, ThemeProvider } from "./Context"; // Import ThemeProvider
import { UserProvider } from './UserContext';
import Home from './components/Home';
import About from './components/About';
import Create from './components/Create';
import Edit from './components/Edit';
import Delete from './components/Delete';
import Searchs from './components/Searchs';
import SelectExam from './components/SelectExam';
import Exam from './components/Exam';
import SearchResult from './components/SearchResult';
import VoiceToText from './components/VoiceToText';
import Search from './components/Search';
import AppBars from './components/AppBar';
import UserSetting from './components/UserSetting';
import Profile from './components/Profile';
import ProfileEdit from './components/ProfileEdit';
import "./App.css";
const AuthPage = () => {
  const [currentForm, setCurrentForm] = useState('login');
  const toggleForm = (formName) => {
    setCurrentForm(formName);
  };

  return (
    <div className="authContainer">
      {currentForm === "login" ? <Login onFormSwitch={() => toggleForm('register')} /> : <Register onFormSwitch={() => toggleForm('login')} />}
    </div>
  );
};

const AppContent = () => {
  const theme = useContext(themeContext);
  const darkMode = theme.state.darkMode;
  const location = useLocation();

  return (
    <div className="App" style={{ background: darkMode ? "black" : "", color: darkMode ? "white" : "" }}>
      {location.pathname !== "/auth" && <Navbar />}
      <Routes>
        <Route exact path="/" element={
          <>
            <Intro />
            <Services />
            <Experience />
            <Works />
            <Portfolio />
            <Testimonial />
            <Contact />
            <Footer />
          </>
        } />
        <Route path="/auth" element={<AuthPage />} />
        <Route path="/create" element={<Create />} />
        <Route path="/about" element={<About />} />
        <Route path="/edit/:id" element={<Edit />} />
        <Route path="/delete/:id" element={<Delete />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/selectexam" element={<SelectExam />} />
        <Route path="/exam" element={<Exam />} />
        <Route path="/searchs" element={<Searchs />} />
        <Route path="/search_result" element={<SearchResult />} />
        <Route path="/voice" element={<VoiceToText />} />
        <Route path="/search" element={<Search />} />
        <Route path="/usersetting" element={<UserSetting />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/profileEdit" element={<ProfileEdit />} />
      </Routes>
    </div>
  );
};

function App() {
  return (
      <Router>
        <UserProvider>
          <AppContent />
        </UserProvider>
      </Router>
  );
}

export default App;
