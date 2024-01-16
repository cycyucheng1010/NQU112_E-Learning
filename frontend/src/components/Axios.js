import axios from 'axios'

const baseUrl ='http://172.17.19.114:8000/'
const AxiosInstance =axios.create({
    baseURL:baseUrl,
    timeout:5000,
    headers:{
        "Content-Type":"application/json",
        accept:"application/json"
    },
    withCredentials: true,
})
export default AxiosInstance