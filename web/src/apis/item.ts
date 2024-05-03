import { request } from '@/utils/axios'

export async function allItemTypeApi (params: any) {
  return request('/bike-shop/item_type/get_itemType', params, 'GET')
}

export async function getItemTypesByBikeApi (params: any) {
  return request('/bike-shop/item_type/get_item_type/', params, 'GET')
}

export async function getBikesByBikeApi (params: any) {
  return request('/bike-shop/item/get_bikes/', params, 'GET')
}

export async function addItemApi (params: any) {
  return request('/bike-shop/item/add_item/', params, 'POST')
}

export async function getItemApi (params: any) {
  return request('/bike-shop/item/get_item/', params, 'GET')
}

export async function searchItemApi (params: any) {
  return request('/bike-shop/item/search_item', params, 'GET')
}

export async function getItemsByTypeApi (params: any) {
  return request('/bike-shop/item/get_items_by_type/', params, 'GET')
}

export async function getMerchantItemApi (params: any) {
  return request('/bike-shop/item/get_merchant_item/', params, 'GET')
}

export async function getRecommendItemApi (params: any) {
  return request('/bike-shop/item/get_recommend_item/', params, 'GET')
}

export async function editItemApi (params: any) {
  return request('/bike-shop/item/edit_item/', params, 'POST')
}

export async function deleteItemApi (params: any) {
  return request('/bike-shop/item/delete_item/', params, 'GET')
}

// 未完成
export async function buySingleItemApi (params: any) {
  return request('/bike-shop/item/', params, 'POST')
}

export async function addItemDescApi (params: any) {
  return request('/bike-shop/item_desc/add_desc/', params, 'POST')
}

export async function editItemDescApi (params: any) {
  return request('/bike-shop/item_desc/edit_desc/', params, 'POST')
}
