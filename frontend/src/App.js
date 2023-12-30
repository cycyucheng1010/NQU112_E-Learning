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

    </Routes>
      }/>
    </div>
  );
}

export default App;