import { request } from '@/utils/axios'

export async function getAnnouncementsApi (params: any) {
  return request('/bike-shop/announcement', params, 'GET')
}
