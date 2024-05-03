import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/HomePage/HomePage.vue')
  },
  // {
  //   path: '/home',
  //   name: 'home',
  //   component: () => import('@/views/HomePage/HomePage.vue')
  // },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/LoginView.vue')
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('@/views/RegisterView.vue')
  },
  {
    path: '/forget_password',
    name: 'forget_password',
    component: () => import('@/views/ForgetPasswordView.vue')
  },
  {
    path: '/change_password',
    name: 'change_password',
    component: () => import('@/views/MyPage/ChangePassword.vue')
  },
  {
    path: '/goods',
    name: 'goods',
    component: () => import('@/views/GoodsView.vue')
  },
  {
    path: '/diy',
    name: 'diy',
    component: () => import('@/views/DiyPage/DiyView.vue')
  },
  {
    path: '/search',
    name: 'search',
    component: () => import('@/views/SearchView.vue')
  },
  {
    path: '/my_page',
    name: 'my_page',
    component: () => import('@/views/MyPage/MyPage.vue')
  },
  {
    path: '/my',
    name: 'my',
    component: () => import('@/views/MyPage/MyView.vue')
  },
  {
    path: '/my_orders',
    name: 'my_orders',
    component: () => import('@/views/MyPage/MyOrdersView.vue')
  },
  {
    path: '/my_address',
    name: 'my_address',
    component: () => import('@/views/MyPage/MyAddressView.vue')
  },
  {
    path: '/merchant_orders',
    name: 'merchant_orders',
    component: () => import('@/views/MyPage/MerchantOrdersView.vue')
  },
  {
    path: '/my_settings',
    name: 'my_settings',
    component: () => import('@/views/MyPage/MySettingsView.vue')
  },
  {
    path: '/add_item',
    name: 'add_item',
    component: () => import('@/views/ItemPage/AddItemView.vue')
  },
  {
    path: '/edit_item',
    name: 'edit_item',
    component: () => import('@/views/ItemPage/EditItemView.vue')
  },
  {
    path: '/list_item',
    name: 'list_item',
    component: () => import('@/views/ItemPage/ListItemView.vue')
  },
  {
    path: '/item_detail',
    name: 'item_detail',
    component: () => import('@/views/ItemPage/ItemDetailView.vue')
  },
  {
    path: '/cart',
    name: 'cart',
    component: () => import('@/views/CartView.vue')
  },
  {
    path: '/order',
    name: 'order',
    component: () => import('@/views/OrderView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
