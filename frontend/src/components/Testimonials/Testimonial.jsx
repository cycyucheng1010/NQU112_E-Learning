import React from "react";
import "./Testimonial.css";
import { Swiper, SwiperSlide, } from "swiper/react";
import "swiper/css";

import { Pagination } from 'swiper/modules';
import "swiper/css/pagination";

const Testimonial = () => {
  const clients = [
    {
      img: "/img/profile1.jpg",
      review:
        "Learning English from an early age is a sensitive period for language acquisition, cognitive development, international perspective, and easier learning of other languages ​​to enhance employment competitiveness and cultural understanding.",
    },
    {
      img: "/img/profile2.jpg",
      review:
        "IELTS (International English Language Testing System) is an internationally accepted English language proficiency testing system designed to assess the English skill level of non-native English speakers.",
    },
    {
      img: "/img/profile3.jpg",
      review:
        "SAT (Scholastic Assessment Test) is a standardized test widely used for American high school students to apply for admission. SAT scores are often an important reference in the college admissions process, especially in the United States.",
    },
    {
      img: "/img/profile4.jpg",
      review:
        "ACT (American College Testing) is an American standardized test mainly used for college admission applications. Like the SAT, the ACT test is designed to assess a student's academic achievement and college readiness.",
    },
  ];

  return (
    <div className="t-wrapper" id="testimonial">
      <div className="t-heading">
        <span>Learn English  </span>
        <span>0 basics </span>
        <span>easily with</span>
      <div className="blur t-blur1" style={{ background: "var(--purple)" }}></div>
      <div className="blur t-blur2" style={{ background: "skyblue" }}></div>

      </div>
      <Swiper
        // install Swiper modules
        modules={[Pagination]}
        slidesPerView={1}
        pagination={{ clickable: true }}
      >
        {clients.map((client, index) => {
          return (
            <SwiperSlide key={index}>
              <div className="testimonial">
                <img src={client.img} alt="" />
                <span>{client.review}</span>
              </div>
            </SwiperSlide>
          );
        })}
      </Swiper>
    </div>
  );
};

export default Testimonial;
