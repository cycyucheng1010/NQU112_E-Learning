import React, { useRef, useState } from "react";

const Profile = () =>{
    const Menus =["Edit Profile","Setting","Logout"];
    const [open,setOpen] =useState(false);

    const menuRef =useRef();
    const imgRef =useRef();

    window.addEventListener("click",(e)=>{
        if (e.target !== menuRef.current && e.target !== imgRef.current){
            setOpen(false);
        }
    });
    
    return(
     <div>
        <div className="profile">
            <img src="/img/user.jpg" alt="User" 
            className="profile-image"
            ref={imgRef}
            onClick={()=>setOpen(!open)}
             />
            {open && (
        <div className="profile-list"
        ref={menuRef}>
            <ul style={{ padding: '0px' }}>
                {Menus.map((menu)=>(
                        <li 
                        onClick={()=>setOpen(false)}
                        className ="profile-text" 
                        key={menu}>{menu}
                        </li>
                    ))}
            </ul>
        </div>
        )}
        </div>
    </div>
    )
};

export default Profile