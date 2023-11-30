import {React,useEffect}  from "react"
import { Box,Typography,Button } from "@mui/material"
import MyDatePickerField from "./forms/MyDatePickerFiled"
import MyMultilineFields from "./forms/MyMultilineField"
import MySelectField from "./forms/MySelectField"
import MyTextfield from "./forms/MyTextField"
import {useForm} from 'react-hook-form'
import AxiosInstance from "./Axios"
import  Dayjs from "dayjs"
import {useNavigate,useParams} from 'react-router-dom'
const Edit =() => {
    const MyParam = useParams()
    const MyId = MyParam.id
    const GetData = () => {
        AxiosInstance.get(`project/${MyId}`).then((res) =>{
          console.log(res.data)
          setValue('name',res.data.name)
          setValue('status',res.data.status)
          setValue('comments',res.data.comments)
          setValue('start_date',Dayjs(res.data.start_date))
          setValue('end_date',Dayjs(res.data.end_date))

     
        })
    
      }
    
      useEffect(() => {
        GetData();
      },[] )
    
    const navigate =useNavigate()
    const defaultValues = {
        name :'',
        comments :'',
        status :'',
        }
    const {handleSubmit,setValue,control} =useForm({defaultValues})
    const submission =(data) => {
        const StartDate = data.start_date && Dayjs(data.start_date["$d"]).format("YYYY-MM-DD");
        const EndDate = data.end_date && Dayjs(data.end_date["$d"]).format("YYYY-MM-DD");


        AxiosInstance.put(`project/${MyId}/`,{
            name:data.name,
            status:data.status, 
            comments:data.comments,
            start_date:StartDate,
            end_date:EndDate,
        })
        .then((res) => {
           navigate('/')
        })
        
    }
    return(
        <div>
            <form onSubmit={handleSubmit(submission)}>
        <Box sx={{display:'flex',width:'100%',backgroundColor:'#00003f',marginBottom:'10px'}}>
            <Typography sx={{marginLeft:'20px',color:'#fff'}}>
               Create records
            </Typography>
        </Box>

        <Box sx={{display:'flex',width:'100%',boxShadow:3,padding:4,flexDirection:'column'}}>


        <Box sx={{display:'flex', justifyContent:'space-around',marginBottom:'40px'}}>
            <MyTextfield
              label="Name"
              name="name"
              control={control}
              placeholder="Provide a project name"
              width={'30%'}
            />

            <MyDatePickerField
             label="Start date"
             name="start_date"
             control={control}
             width={'30%'}
            />

            <MyDatePickerField
             label="End date"
             name="end_date"
             control={control}
             width={'30%'}
            />

        </Box>
        
        <Box sx={{display:'flex', justifyContent:'space-around',marginBottom:'40px'}}>
            <MyMultilineFields
              label="Comments"
              name="comments"
              control={control}
              placeholder="Provide a project Comments"
              width={'30%'}
            />

            <MySelectField
             label="Status"
             name="status"
             control={control}
             width={'30%'}
            />

            <Box sx={{width:'30%'}}>
                <Button variant="contained" type="submit" sx={{width:'100%'}}>
                    Submit
                </Button>
            </Box>

            

        </Box >
        
        
        
        
        </Box>
        </form>
     </div>
)
}

export default Edit