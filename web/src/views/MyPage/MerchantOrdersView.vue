<template>
  <div class="MerchantOrder">
    <div class="Container">
      <el-card class="MerchantOrderPanel">
        <template #header>
          <el-button class="backButton" type="default" round @click="backPage"
            ><el-icon class="MyNavUnitIcon"><ArrowLeft /></el-icon
            >返回</el-button
          >
          <span class="CardHeader">订单列表</span></template
        >
        <div class="MerchantOrderContent">
          <div
            class="OrderItemsUnit"
            v-for="(item, index) in OrdersProfile.data"
            :key="index"
          >
            <el-descriptions class="OrderProfile" title="订单信息" border>
              <el-descriptions-item label="订单号:">
                {{ item.order_id }}
              </el-descriptions-item>
              <el-descriptions-item label="电话:">
                {{ item.order.phone }}
              </el-descriptions-item>
              <el-descriptions-item label="地址:">
                {{ item.order.address }}
              </el-descriptions-item>
            </el-descriptions>
            <div class="ItemProfile">
              <div class="itemImg">
                <img :src="baseURL + item.item_image" alt="" height="100%" />
              </div>
              <div class="itemProfile">
                <el-descriptions :title="item.item_name">
                  <el-descriptions-item label="商品种类:">{{
                    item.item_type
                  }}</el-descriptions-item>
                  <el-descriptions-item label="数量:">{{
                    item.quantity
                  }}</el-descriptions-item>
                  <el-descriptions-item label="购买单价:">{{
                    item.price
                  }}</el-descriptions-item>
                  <el-descriptions-item label="所属订单号:">{{
                    item.order_id
                  }}</el-descriptions-item>
                  <el-descriptions-item label="状态:">{{
                    item.status_name
                  }}</el-descriptions-item>
                  <el-descriptions-item label="操作:"
                    ><el-button
                      round
                      type="primary"
                      @click="changeStatus(item, index)"
                      :disabled="
                        item.status === 'tobepaid' ||
                        item.status === 'delivered' ||
                        item.status === 'confirmed' ||
                        item.status === 'commented'
                          ? true
                          : false
                      "
                      >下一步</el-button
                    >
                  </el-descriptions-item>
                  <el-descriptions-item
                    label="评价:"
                    v-if="item.status === 'commented'"
                    >{{ item.comment }}</el-descriptions-item
                  >
                </el-descriptions>
              </div>
            </div>
          </div>
        </div>
      </el-card>
    </div>
  </div>

  <!-- 签收窗口 -->
  <el-dialog
    v-model="signDialog"
    title="更新订单进度"
    width="500"
    class="dialog"
  >
    <span>确认进入下一个状态？</span>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="signDialog = false" round>Cancel</el-button>
        <el-button type="primary" @click="handleChange" round> 确定 </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script lang="ts" setup>
import { onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft } from '@element-plus/icons-vue'
import {
  getOrdersApi as getOrders,
  getMerchantOrdersApi as getMerchantOrders,
  deleteSingleOrderApi as deleteSingleOrder,
  changeOrderStatusApi as changeOrderStatus
} from '@/apis/order'
import baseURL from '@/utils/axios'
import { ElMessage } from 'element-plus'

const router = useRouter()
const OrdersProfile = reactive({ data: [] })

// 返回键的操作
const backPage = () => {
  router.back()
}

const toPage = (param: string) => {
  const name = param.toString()
  router.push({ name: name })
}

const getMerchantOrdersProfile = () => {
  return getMerchantOrders({
    token: localStorage.getItem('TOKEN')
  })
    .then((res: any) => {
      OrdersProfile.data = res.data.data
      // console.log(res)
    })
    .catch((err: any) => {
      console.log(err)
    })
}

// 加载页面时候获取购物车物品详细数据
onMounted(async () => {
  try {
    await getMerchantOrdersProfile()
  } catch (error) {
    console.error(error)
  }
})

// 订单状态修改
const toHandleOrderItem = reactive({ index: 0, data: {} })
const signDialog = ref(false)
const changeStatus = (item: any, index: any) => {
  toHandleOrderItem.data = item
  toHandleOrderItem.index = index
  signDialog.value = true
}

// 删除订单
const deleteOrder = (orderId: any) => {
  return deleteSingleOrder(orderId)
    .then((res) => {
      console.log(res)
    })
    .catch((err) => {
      console.log(err)
    })
}

const handleChange = () => {
  // 判断订单状态和新状态
  let newStatus = ''
  if (toHandleOrderItem.data.status_name === '订单准备中') {
    newStatus = 'sent'
  } else if (toHandleOrderItem.data.status_name === '已发货') {
    newStatus = 'shipping'
  } else if (toHandleOrderItem.data.status_name === '运送中') {
    newStatus = 'delivered'
  }
  // 提起订单状态更改请求

  changeOrderStatus({
    orderItemId: toHandleOrderItem.data.orderdetail_id,
    newStatus: newStatus
  })
    .then((res) => {
      ElMessage.success('更新成功！')
      getMerchantOrdersProfile()
    })
    .catch((err) => {
      console.log(err)
    })
  signDialog.value = false
}
</script>
<script lang="ts">
export default {}
</script>

<style lang="less" scoped>
@import '@/assets/styles/common.css';
.MerchantOrder {
  min-height: 100%;
  margin: 0;
  background-color: #f0f0f0;

  .Container {
    padding: 15px;
    .MerchantOrderPanel {
      border-radius: 25px;
      padding: 20px;
      .backButton {
        float: left;
      }

      .MerchantOrderContent {
        .OrderItemsUnit {
          // display: flex;
          margin: 10px 0;
          padding: 10px;
          border-radius: 25px;
          border: 1px solid #e7e7e7;

          .OrderProfile {
            padding: 20px;
          }

          .ItemProfile {
            display: flex;

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
      }

      .settleButton {
        float: right;
      }
    }
  }
}
</style>
