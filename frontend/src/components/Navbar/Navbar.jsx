import React from "react";
import Toggle from "../Toggle/Toggle";
import "./Navbar.css";
import { Link as ScrollLink } from "react-scroll"; // 重命名以避免冲突
import { Link as RouterLink } from "react-router-dom"; // 导入 react-router-dom 的 Link
import { useUser } from '../../UserContext';


const Navbar = () => {
  const { user } = useUser(); // 获取当前用户信息

  return (
    <div className="n-wrapper" id="Navbar">
      {/* left */}
      <div className="n-left">
        <div className="n-name">English</div>
        <Toggle />
      </div>
      {/* right */}
      <div className="n-right">
        <div className="n-list">
          <ul style={{ listStyleType: "none" }}>
            <li>
              <ScrollLink activeClass="active" to="Navbar" spy={true} smooth={true}>
                Home
              </ScrollLink>
            </li>
            <li>
              <ScrollLink to="services" spy={true} smooth={true}>
                Services
              </ScrollLink>
            </li>
            <li>
              <ScrollLink to="works" spy={true} smooth={true}>
                Experience
              </ScrollLink>
            </li>
            <li>
              <ScrollLink to="portfolio" spy={true} smooth={true}>
                Portfolio
              </ScrollLink>
            </li>
            <li>
              <ScrollLink to="testimonial" spy={true} smooth={true}>
                Testimonial
              </ScrollLink>
            </li>
          </ul>
        </div>
        <RouterLink to="/auth">
        <button className="button n-button">
                {user ? user.name : 'Login/Logout'} {/* 若要針對 LOGIN/LOGOUT 的案件做修正*/}
            </button>
        </RouterLink>
      </div>
    </div>
  );
};

export default Navbar;
