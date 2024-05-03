import { request } from '@/utils/axios'

// 注册接口
export async function registerApi (params: any) {
  return request('/bike-shop/user/register/', params, 'POST')
}
