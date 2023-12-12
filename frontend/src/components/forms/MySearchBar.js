import * as React from 'react';
import { FaSearch } from "react-icons/fa";
import "./css/SearchBar.css";
import AxiosInstance from "../Axios";
import { Controller } from 'react-hook-form';

export default function MySearchBar(props) {
  const{label,placeholder,width,name,control} = props   
return (
  
    <div className="input-wrapper">
      <FaSearch id="search-icon" />
      <input
        placeholder="輸入以搜索"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onBlur={() => fetchData(input)}
      />
    </div>
  );
};
