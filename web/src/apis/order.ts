import { request } from '@/utils/axios'

export async function orderSingleItemApi (params: any) {
  return request('/bike-shop/order/order_single_item/', params, 'POST')
}

export async function deleteSingleOrderApi (params: any) {
  const url = '/bike-shop/order/' + params.toString()
  return request(url, {}, 'DELETE')
}

export async function getOrderItemsApi (params: any) {
  return request('/bike-shop/order/get_items/', params, 'POST')
}

export async function orderItemsApi (params: any) {
  return request('/bike-shop/order/order_items/', params, 'POST')
}

export async function getOrdersApi (params: any) {
  return request('/bike-shop/order/get_orders/', params, 'GET')
}

export async function getMerchantOrdersApi (params: any) {
  return request('/bike-shop/order/get_merchant_orders/', params, 'GET')
}

export async function changeOrderStatusApi (params: any) {
  return request('/bike-shop/order/change_order_status/', params, 'POST')
}

export async function commentOrderApi (params: any) {
  return request('/bike-shop/order/comment_order/', params, 'POST')
}
