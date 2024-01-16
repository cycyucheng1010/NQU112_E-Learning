import React, { useState,useCallback  } from "react";
import "./Searchs.css";
import SearchIcon from '@mui/icons-material/Search';
import CloseIcon from '@mui/icons-material/Close';
import AxiosInstance from './Axios';
import axios from 'axios'; 
import { useNavigate } from 'react-router-dom';
import _ from 'lodash';  // 引入防抖

function Searchs({ placeholder, data }) {
  const [filteredData, setFilteredData] = useState([]);
  const [wordEntered, setWordEntered] = useState("");
  const [isSearching, setIsSearching] = useState(false);
  const navigate = useNavigate(); 

  const handleFilter = (event) => {
    const searchWord = event.target.value;
    setWordEntered(searchWord);
  
    if (searchWord.trim() === "") {
      setFilteredData([]);
    } else {
      AxiosInstance.get(`search/?search_word=${encodeURIComponent(searchWord.trim())}`)
        .then((response) => {
          setFilteredData(response.data);
          console.log(response.data);
        })
        .catch((error) => {
          console.error("Error fetching the data: ", error);
        });
    }
  };

  const debouncedSearchWord = useCallback(_.debounce((word) => {
    if (!word.trim() || isSearching) return;
    setIsSearching(true);

    let url = 'http://localhost:8000/result/receive_word/';
    axios.post(url, { word: word }, { headers: { 'Content-Type': 'application/json' } })
      .then(response => {
        console.log('后端响应:', response);
        navigate('/search_result');
      })
      .catch(error => {
        console.error("Error posting the data: ", error);
      })
      .finally(() => {
        setIsSearching(false);  // 请求完成后，重置搜索状态
      });
  }, 300), []);  // 300毫秒的延迟

  const clearInput = () => {
    setFilteredData([]);
    setWordEntered("");
  };

  return (
    <div className="search">
      <div className="searchInputs">
        <input
          type="text"
          placeholder={placeholder}
          value={wordEntered}
          onChange={handleFilter}
        />
        <div className="searchIcon">
          {filteredData.length === 0 ? (
            <SearchIcon />
          ) : (
            <CloseIcon id="clearBtn" onClick={clearInput} />
          )}
        </div>
      </div>
      {filteredData.length !== 0 && (
        <div className="dataResult">
          {filteredData.slice(0, 15).map((word, index) => {
             return (
                <a 
                  className="dataItem" 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  key={index}
                  onClick={() => debouncedSearchWord(word)}  // 使用防抖函数
                >
                  {word}
                </a>
             );
          })}
        </div>
      )}
    </div>
  );
}

export default Searchs;
