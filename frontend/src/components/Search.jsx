import React, { useState } from "react";
import "./Searchs.css";
import SearchIcon from '@mui/icons-material/Search';
import CloseIcon from '@mui/icons-material/Close';
import AxiosInstance from './Axios';

function Search({ placeholder, data }) {
  const [filteredData, setFilteredData] = useState([]);
  const [wordEntered, setWordEntered] = useState("");

  const handleFilter = (event) => {
    const searchWord = event.target.value;
    setWordEntered(searchWord);
  
    if (searchWord.trim() === "") {
      setFilteredData([]);
    } else {
      // 使用 AxiosInstance 向后端 API 发送请求
      AxiosInstance.get(`search/?search_word=${encodeURIComponent(searchWord.trim())}`)
        .then((response) => {
          // 后端返回的数据是一个单词列表
          setFilteredData(response.data);
          console.log(response.data);
        })
        .catch((error) => {
          console.error("Error fetching the data: ", error);
        });
    }
  };

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
             // 构建目标链接，这里假设是一个词典网站。
             const wordLink = `https://dictionary.cambridge.org/dictionary/english-chinese-traditional/${word}`;
             return (
                <a 
                  className="dataItem" 
                  href={wordLink} 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  key={index}
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

export default Search;
