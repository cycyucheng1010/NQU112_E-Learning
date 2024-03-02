import React, { useState } from "react";
import { Dialog } from 'primereact/dialog'; 
import { Button } from "primereact/button";      
import Avatar from "react-avatar-edit";
import DownloadDoneIcon from '@mui/icons-material/DownloadDone';
import { Box } from "@mui/material";
import TextField from "@mui/material/TextField";
import Input from "@mui/material/Input";
import EditIcon from '@mui/icons-material/Edit';

const ProfileEdit = () =>{
    const [imagecrop, setimagecrop] = useState(false);
    const [image, setimage] = useState("");
    const [src, setsrc] = useState(false);
    const [profile, setprofile] = useState([]);
    const [pview, setpview] = useState(false);
    const [dynamicText, setDynamicText] = useState('hello');
    const [isEditing, setIsEditing] = useState(false); // 控制輸入框是否可編輯
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const profileFinal = profile.map((item) => item.pview);

    const onClose = () =>{
        setpview(null);
    };

    const onCrop = (view) => {
        setpview(view);
    };

    const saveCropImage = (e) =>{
        e.preventDefault(); // 阻止表單的默認提交行為
        setprofile([...profile,{ pview }]);
        setimagecrop(false);
    };

    const handleChangeText = (event) =>{
        setDynamicText(event.target.value);
    };

    const toggleEditing = () => {
        setIsEditing(prev => !prev);
    };

    return(
        <div style={{
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    padding: '1rem'
                }}>
            <div style={{
                        textAlign: "center",
                        display: "flex",
                        flexDirection:"column",
                        justifyContent:"center",
                        alignItems:"center",
                    }}>
                <img
                    style={{
                        width:"200px",
                        height:"200px",
                        borderRadius:"50%",
                        objectFit:"cover",
                        border:"4px solid green",
                        textAlign: "center",
                        cursor: "pointer",
                    }}
                    onClick={()=> setimagecrop(true)}
                    src="/img/user.jpg" alt=""/>
                
                <div style={{ display: 'flex', alignItems: 'center', marginTop: '16px' }}>
                    <Input
                        value={dynamicText}
                        onChange={handleChangeText}
                        disabled={!isEditing} // 根據編輯狀態控制輸入框是否可編輯
                        inputProps={{
                            style: {
                                textAlign: 'center',
                                fontSize: '32px',
                                fontWeight: '600',
                            },
                        }}
                    />
                    <div style={{ marginLeft: '8px' }}> {/* 按鈕的 div 容器 */}
                        <Button variant="contained" onClick={toggleEditing}>
                            <EditIcon />
                        </Button>
                    </div>
                </div>
                
                <TextField
                    id="username"
                    label="帳號"
                    value={username}
                    onChange={(event) => setUsername(event.target.value)}
                    variant="outlined"
                    style={{ marginTop: '16px' }}
                />

                <TextField
                    id="password"
                    label="密碼"
                    type="password"
                    value={password}
                    onChange={(event) => setPassword(event.target.value)}
                    variant="outlined"
                    style={{ marginTop: '16px' }}
                />
                    
                <Dialog
                    visible={imagecrop}
                    header="Update Profile"
                    style={{ fontSize: '2rem', fontWeight: '600', color: 'black', backgroundColor:'white', border:"2px solid grey" }}
                    onHide={() => setimagecrop(false)}
                >
                    <div style={{ display:"flex", flexDirection:'column', alignItems:"center", backgroundColor:"white" }}>
                        <Avatar
                            width={500}
                            height={400}
                            onCrop={onCrop}
                            onClose={onClose}
                            src={src}
                        />
                        <div style={{ display:"flex", flexDirection:"column", alignItems:"center", marginTop:"1.25rem", width:"3rem" }}>
                            <div style={{ display:"flex", justifyContent:'space-around', marginTop:"1rem", width:"4rem" }}>
                                <Button
                                    style={{
                                        border: "2px solid grey",
                                        backgroundColor: "#ADD8E6",
                                        color: "white",
                                        padding: "10px 20px",
                                        display: "flex",
                                        alignItems: "center",
                                        textAlign: "left",
                                        textDecoration: "none",
                                        fontSize: "16px",
                                        margin: "4px 2px",
                                        cursor: "pointer",
                                        borderRadius: "12px",
                                        minWidth: "120px"
                                    }}
                                    onClick={saveCropImage}
                                    icon={<DownloadDoneIcon style={{ marginRight: '8px' }} />}
                                    label="Save"
                                />
                            </div>
                        </div>
                    </div>
                </Dialog>

                <input // input 元素，用於上傳圖片
                    type="file" 
                    accept="/image/*"
                    style={{ display:"none", backgroundColor:"white" }}
                    onChange={(event)=>{
                        const file = event.target.files[0];
                        if(file && file.type.substring(0,5) === 'image'){
                            setimage(file);
                        } else {
                            setimage(null)
                        }
                    }}
                />
            </div>
        </div>
    );
}

export default ProfileEdit;
