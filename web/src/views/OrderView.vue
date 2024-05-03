<template>
  <div class="Order">
    <div class="Container">
      <el-card class="OrderPanel">
        <template #header>
          <el-button class="backButton" type="default" round @click="backPage"
            ><el-icon class="MyNavUnitIcon"><ArrowLeft /></el-icon
            >返回</el-button
          >
          <span class="CardHeader">确认订单</span></template
        >
        <div class="OrderContent">
          <div class="OrderInfo">
            <el-descriptions title="订单信息">
              <el-descriptions-item label="姓名">{{
                OrderProfile.user.username
              }}</el-descriptions-item>
              <el-descriptions-item label="邮箱">{{
                OrderProfile.user.email
              }}</el-descriptions-item>
              <el-descriptions-item label="电话">
                <el-input
                  v-model="OrderProfile.user.phone"
                  :placeholder="OrderProfile.user.phone"
                  style="width: 240px"
                ></el-input>
              </el-descriptions-item>
              <el-descriptions-item label="递送地址">
                <el-input
                  v-model="OrderProfile.user.address"
                  :placeholder="OrderProfile.user.address"
                ></el-input>
              </el-descriptions-item>
            </el-descriptions>
          </div>
          <div
            class="OrderUnit"
            v-for="(item, index) in OrderProfile.data"
            :key="index"
          >
            <div class="itemImg">
              <img :src="baseURL + item.item_image" alt="" height="100%" />
            </div>
            <div class="itemProfile">
              <el-descriptions :title="item.item_name">
                <el-descriptions-item label="商品种类:">{{
                  item.item_type
                }}</el-descriptions-item>
                <el-descriptions-item label="数量:" v-if="orderType === 'cart'">
                  {{ item.quantity }}
                </el-descriptions-item>
                <el-descriptions-item label="数量:" v-else>
                  {{ quantity }}
                </el-descriptions-item>
                <el-descriptions-item label="价格:">{{
                  item.price
                }}</el-descriptions-item>
                <el-descriptions-item label="小计:" v-if="orderType === 'cart'"
                  >￥ {{ (item.price * item.quantity).toFixed(2) }}
                </el-descriptions-item>
                <el-descriptions-item label="小计:" v-else
                  >￥ {{ OrderProfile.total }}
                </el-descriptions-item>
              </el-descriptions>
            </div>
          </div>
        </div>
        <template #footer>
          <span class="CardFooter" style="float: left"
            >总价：￥{{ OrderProfile.total }}</span
          >
          <el-button
            class="settleButton"
            type="primary"
            round
            @click="submitOrder"
          >
            提交订单
          </el-button>
        </template>
      </el-card>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft } from '@element-plus/icons-vue'
import {
  getOrderItemsApi as getOrderItems,
  orderItemsApi as orderItems
} from '@/apis/order'
import { getItemApi as getItem } from '@/apis/item'
import { userProfileApi as userProfile } from '@/apis/user'
import baseURL from '@/utils/axios'

const router = useRouter()
const route = useRoute()
const OrderProfile = reactive({ data: [], total: '', user: {} })

// 进入确认订单页面需要获取所对应的商品id
const itemsId = route.query.itemsId
const orderType = route.query.type
const quantity = parseInt(route.query.quantity as string)

// 返回键的操作
const backPage = () => {
  router.back()
}

const toPage = (param: string) => {
  const name = param.toString()
  router.push({ name: name })
}

const getMyData = async () => {
  return await userProfile({ token: localStorage.getItem('TOKEN') })
    .then((res: any) => {
      // console.log(res)
      OrderProfile.user = res.data.data
    })
    .catch((err) => {
      console.log(err)
      throw err
    })
}

// 购物车结算获取信息
const getCartProfile = () => {
  return getOrderItems({
    token: localStorage.getItem('TOKEN'),
    orderItems: itemsId
  })
    .then((res: any) => {
      OrderProfile.data = res.data.data
      OrderProfile.total = res.data.total
      console.log(OrderProfile.data)
    })
    .catch((err: any) => {
      console.log(err)
    })
}

// 详情页面直接结算获取信息
const getItemProfile = () => {
  return getItem({ itemId: itemsId })
    .then((res: any) => {
      OrderProfile.data.push(res.data.data)
      OrderProfile.total = (parseFloat(res.data.data.price) * quantity)
        .toFixed(2)
        .toString()
      console.log(OrderProfile.data)
    })
    .catch((err) => {
      console.error(err)
      throw err
    })
}

const submitOrder = () => {
  const orderingItems = [] as any
  // 购物车提交
  if (orderType === 'cart') {
    OrderProfile.data.forEach((element) => {
      orderingItems.push({
        itemId: element.item_id,
        quantity: element.quantity,
        price: element.price
      })
    })
  } else {
    // 直接下单
    OrderProfile.data.forEach((element) => {
      orderingItems.push({
        itemId: element.item_id,
        quantity: quantity,
        price: element.price
      })
    })
    console.log(orderingItems)
  }

  return orderItems({
    token: localStorage.getItem('TOKEN'),
    address: OrderProfile.user.address,
    phone: OrderProfile.user.phone,
    orderItems: orderingItems,
    total: OrderProfile.total,
    orderType: orderType
  })
    .then((res) => {
      toPage('my_page')
      console.log(res)
    })
    .catch((err) => {
      console.log(err)
    })
}

// 加载页面时候获取购物车物品详细数据
onMounted(async () => {
  try {
    if (orderType === 'cart') {
      await getCartProfile()
    } else await getItemProfile()
    await getMyData()
  } catch (error) {
    console.error(error)
  }
})

// 确认或者输入新地址

// 提交购物车表单生成订单
</script>
<script lang="ts">
export default {}
</script>

<style lang="less" scoped>
@import '@/assets/styles/common.css';
.Order {
  min-height: 100%;
  margin: 0;
  background-color: #f0f0f0;

  .Container {
    padding: 15px;
    .OrderPanel {
      border-radius: 25px;
      padding: 20px;
      .backButton {
        float: left;
      }

      .OrderContent {
        .OrderInfo {
          margin-bottom: 10px;
          padding: 10px;
        }

        .OrderUnit {
          display: flex;
          margin-bottom: 10px;
          padding: 10px;
          border: 1px solid #e7e7e7;
          border-radius: 25px;
          .itemImg {
            display: inline-block;
            width: 125px;
            height: 125px;
            border: 1px solid #e7e7e7;
            border-radius: 15px;
            overflow: hidden;
          }
          .itemProfile {
            display: inline-block;
            min-width: 600px;
            padding-left: 20px;
          }
          .itemAction {
            margin-left: auto;
          }
        }
      }

      .settleButton {
        float: right;
      }
    }
  }
}
</style>
