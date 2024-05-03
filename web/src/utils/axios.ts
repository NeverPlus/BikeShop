import axios from 'axios'
import { ElMessage } from 'element-plus'
import { showMessage } from './status'
// import router from '@/router'
// import { config } from 'vue/types/umd'
// import { reject, resolve } from 'core-js/fn/promise'

// 默认请求地址
const baseURL = 'http://127.0.0.1:8000'

axios.defaults.baseURL = baseURL
axios.defaults.withCredentials = true
axios.defaults.headers['x-requeseted-with'] = 'XMLHttpRequest'
// axios.defaults.headers['X-CSRFToken'] = cookie.parse(document.cookie).rsrftoken
axios.defaults.headers.post['Content-Type'] = 'application/json'

// 接口超时时间
axios.defaults.timeout = 30000

// http请求拦截器
// axios.interceptors.request.use(
//   (config) => {
//     config.headers = {
//       'Content-Type': 'application/json;charset=UTF-8'
//     }
//     return config
//   },
//   (error) => {
//     return Promise.reject(error)
//   }
// )
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('TOKEN')
    const regex = /.*csrftoken=([^;.]*).*$/ // 用于从cookie中匹配 csrftoken值
    const cookie = document.cookie.match(regex)
    if (document.cookie.match(regex) !== null) {
      config.headers['X-CSRFToken'] = cookie[1]
    }
    if (token && token.length > 0) {
      config.headers.Authorization = 'Bearer' + localStorage.getItem('TOKEN')
    }
    return config
  },
  (err) => {
    ElMessage.error('请求超时')
    return Promise.resolve(err)
  }
)

// http回答拦截器
axios.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    const { response } = error
    if (response) {
      showMessage(response.status)
      return Promise.reject(response.data)
    } else {
      ElMessage.warning('网络连接异常，请稍后再试！')
    }
  }
)
export default baseURL

// 封装请求并导出
export function request (url = '', params = {}, type = 'POST') {
  return new Promise((resolve, reject) => {
    let promise: any
    if (type.toUpperCase() === 'GET') {
      promise = axios({
        method: 'GET',
        url: baseURL + url,
        params
      })
    } else if (type.toUpperCase() === 'POST') {
      promise = axios({
        method: 'POST',
        url: baseURL + url,
        data: params
      })
      console.log(baseURL + url)
    } else if (type.toUpperCase() === 'DELETE') {
      promise = axios({
        method: 'DELETE',
        url: baseURL + url,
        data: params
      })
      console.log(baseURL + url)
    }
    promise
      .then((res: any) => {
        resolve(res.data)
      })
      .catch((err: any) => {
        reject(err)
      })
  })
}
