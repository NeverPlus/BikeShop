import { request } from '@/utils/axios'

export async function addCartItemApi (params: any) {
  return request('/bike-shop/cart/add_item/', params, 'POST')
}

export async function addCartItemsApi (params: any) {
  return request('/bike-shop/cart/add_items/', params, 'POST')
}

export async function editCartItemApi (params: any) {
  return request('/bike-shop/cart/edit_item/', params, 'POST')
}

export async function getCartItemApi (params: any) {
  return request('/bike-shop/cart/get_items/', params, 'GET')
}

// export async function deleteCartItemApi (params: any) {
//   const url = '/bike-shop/cart_detail/' + params.toString()
//   return request(url, {}, 'DELETE')
// }

export async function deleteCartItemApi (params: any) {
  return request('/bike-shop/cart/delete_item/', params, 'POST')
}
