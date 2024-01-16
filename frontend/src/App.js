import './App.css';
import {Routes,Route} from 'react-router-dom'
import Home from './components/Home';
import About from './components/About';
import Create from './components/Create';
import Navbar from './components/Navbar';
import Edit from './components/Edit';
import Delete from './components/Delete';
import Searchs from './components/Searchs';
import Login from './components/Login'; 
import Register from './components/Register';
import SelectExam from './components/SelectExam';
import Exam from './components/Exam';
import SearchResult from './components/SearchResult';
import VoiceToText from './components/VoiceToText';
import Search from './components/Search';
import AppBars from './components/AppBar';

function App() {
  const myWidth =200
  return (
    <div className="App">
      <Navbar drawerWidth={myWidth}
      content ={

      <Routes>
      <Route path="" element={<Home/>}/>
      <Route path="/create" element={<Create/>}/>
      <Route path="/about" element={<About/>}/>
      <Route path="/edit/:id" element={<Edit/>}/>
      <Route path="/delete/:id" element={<Delete/>}/>
      <Route path="/login" element={<Login/>}/>
      <Route path="/register" element={<Register/>}/>
      <Route path="/selectexam" element={<SelectExam/>}/>
      <Route path="/exam" element={<Exam/>}/>
      <Route path="/searchs" element={<Searchs/>}/>
      <Route path="/search_result" element={<SearchResult/>}/>
      <Route path="/voice" element={<VoiceToText/>}/>
      <Route path="/search" element={<Search/>}/>

    </Routes>
      }/>
    </div>
  );
}

export default App;