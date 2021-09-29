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
    sorting(column, method, page=1){
        method = method ? 'desc': 'asc'
        return apiClient.get(`/sort/${column}/${method}/${page}/`)
    },
    api(obj){
        return apiClient.get('/api/', {
            params: obj
        })
    }
}