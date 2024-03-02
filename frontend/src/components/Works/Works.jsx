import React, { useContext } from "react";
import "./Works.css";
import { themeContext } from "../../Context";
import { motion } from "framer-motion";
import {Link} from 'react-scroll'
const Works = () => {
  // context
  const theme = useContext(themeContext);
  const darkMode = theme.state.darkMode;

  // transition
  return (
    <div className="works" id="works">
      {/* left side */}
      <div className="w-left">
        <div className="awesome">
          {/* dark Mode */}
          <span style={{ color: darkMode ? "white" : "" }}>
            Works for All these
          </span>
          <span>Design & Function</span>
          <spane>
          An English learning system that accompanies your child's growth, with basic functions and 1-to-1 AI English tutoring to give you the best learning efficiency anytime, anywhere.
            <br />
            
            <br />
            
            <br />
            
          </spane>
          <Link to="contact" smooth={true} spy={true}>
            <button className="button s-button">Hire Me</button>
          </Link>
          <div
            className="blur s-blur1"
            style={{ background: "#ABF1FF94" }}
          ></div>
        </div>

        {/* right side */}
      </div>
      <div className="w-right">
        <motion.div
          initial={{ rotate: 45 }}
          whileInView={{ rotate: 0 }}
          viewport={{ margin: "-40px" }}
          transition={{ duration: 3.5, type: "spring" }}
          className="w-mainCircle"
        >
          <div className="w-secCircle">
            <img src="/img/Upwork.png" alt="" />
          </div>
          <div className="w-secCircle">
            <img src="/img/fiverr.png" alt="" />
          </div>
          <div className="w-secCircle">
            <img src="/img/amazon.png" alt="" />
          </div>{" "}
          <div className="w-secCircle">
            <img src="/img/Shopify.png" alt="" />
          </div>
          <div className="w-secCircle">
            <img src="/img/Facebook.png" alt="" />
          </div>
        </motion.div>
        {/* background Circles */}
        <div className="w-backCircle blueCircle"></div>
        <div className="w-backCircle yellowCircle"></div>
      </div>
    </div>
  );
};

export default Works;
