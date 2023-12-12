import './App.css';
import {Routes,Route} from 'react-router-dom'
import Home from './components/Home';
import About from './components/About';
import Create from './components/Create';
import Navbar from './components/Navbar';
import Edit from './components/Edit';
import Delete from './components/Delete';
import Search from './components/Search';
import Login from './components/Login'; 
import Register from './components/Register';
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
      <Route path="/search" element={<Search/>}/>
      <Route path="/login" element={<Login/>}/>
      <Route path="/register" element={<Register/>}/>
    
    </Routes>
      }/>
    </div>
  );
}

export default App;