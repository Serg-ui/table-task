import axios from 'axios'

const apiClient = axios.create({
    baseURL: 'http://127.0.0.1:5000/',
    withCredentials: false,
    headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json'
    }
})

export default {
    home_page(){
        return apiClient.get('')
    },

    api(obj){
        return apiClient.get('/api/', {
            params: obj
        })
    }
}