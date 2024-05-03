import { request } from '@/utils/axios'

// 登录接口
export async function userProfileApi (params: any) {
  return request('/bike-shop/user/profile/', params, 'GET')
}

export async function userAvatarUpdateApi (params: any) {
  return request('/bike-shop/user/update_avatar/', params, 'POST')
}

export async function userProfileUpdateApi (params: any) {
  return request('/bike-shop/user/update_profile/', params, 'POST')
}

export async function userPasswordUpdateApi (params: any) {
  return request('/bike-shop/user/update_password/', params, 'POST')
}

export async function forgetPasswordApi (params: any) {
  return request('/bike-shop/user/forget_password/', params, 'POST')
}
