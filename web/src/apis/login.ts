import { request } from '@/utils/axios'

// 登录接口
export async function loginApi (params: any) {
  return request('/bike-shop/user/login/', params, 'POST')
}
