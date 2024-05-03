import axios from 'axios'
import { ElMessage } from 'element-plus'
import { showMessage } from './status'

const instance = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  timeout: 30000,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
    'X-Requeset-with': 'XMLHttpRequest'
  }
})

instance.interceptors.request.use(
  (config) => {
    const token = sessionStorage.getItem('Token')
    if (token && token.length > 0) {
      config.headers.Authorization = 'Bearer' + sessionStorage.getItem('Token')
    }
    return config
  },
  (err) => {
    ElMessage.error('请求超时')
    return Promise.resolve(err)
  }
)

// http回答拦截器
instance.interceptors.response.use(
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
export default instance

export function request (url = '', params = {}, type = 'POST') {
  return new Promise((resolve, reject) => {
    let promise: any
    if (type.toUpperCase() === 'GET') {
      promise = axios({
        method: 'GET',
        url,
        params
      })
    } else if (type.toUpperCase() === 'POST') {
      promise = axios({
        method: 'POST',
        url,
        data: params
      })
    }
    promise
      .then((res: any) => {
        resolve(res)
      })
      .catch((err: any) => {
        reject(err)
      })
  })
}
