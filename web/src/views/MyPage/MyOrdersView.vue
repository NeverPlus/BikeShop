<template>
  <div class="MyOrder">
    <div class="Container">
      <el-card class="MyOrderPanel">
        <template #header>
          <el-button class="backButton" type="default" round @click="backPage"
            ><el-icon class="MyNavUnitIcon"><ArrowLeft /></el-icon
            >返回</el-button
          >
          <span class="CardHeader">订单列表</span></template
        >
        <div class="MyOrderContent">
          <el-empty
            description="您还没有订单哦！"
            v-if="Object.keys(OrdersProfile.data).length === 0"
          />
          <div
            v-else
            class="MyOrderUnit"
            v-for="(order, index) in OrdersProfile.data"
            :key="index"
          >
            <el-descriptions class="OrderProfile" border>
              <el-descriptions-item label="订单号:">
                {{ order.order_id }}
              </el-descriptions-item>
              <el-descriptions-item label="总计:">
                ￥{{ order.total }}
              </el-descriptions-item>
              <el-descriptions-item label="电话:">
                {{ order.phone }}
              </el-descriptions-item>
              <el-descriptions-item label="地址:">
                {{ order.address }}
              </el-descriptions-item>
              <el-descriptions-item label="操作"
                ><el-button
                  round
                  type="danger"
                  @click="deleteOrder(order.order_id)"
                  >删除</el-button
                ></el-descriptions-item
              >
            </el-descriptions>
            <div class="OrderItemsBox">
              <div
                class="OrderItemsUnit"
                v-for="(item, i) in order.order_details"
                :key="i"
              >
                <div class="itemImg">
                  <img :src="baseURL + item.item_image" alt="" height="100%" />
                </div>
                <div class="itemProfile">
                  <el-descriptions :title="item.item_name">
                    <el-descriptions-item label="商品种类">{{
                      item.item_type
                    }}</el-descriptions-item>
                    <el-descriptions-item label="数量">{{
                      item.quantity
                    }}</el-descriptions-item>
                    <el-descriptions-item label="购买单价">{{
                      item.price
                    }}</el-descriptions-item>
                    <el-descriptions-item label="订单状态:"
                      >{{ item.status_name }}
                    </el-descriptions-item>
                    <el-descriptions-item label="操作:"
                      ><el-button
                        round
                        type="primary"
                        @click="changeStatus(item, index)"
                        :disabled="
                          item.status === 'tobepaid' ||
                          item.status === 'delivered' ||
                          item.status === 'confirmed'
                            ? false
                            : true
                        "
                        >下一步</el-button
                      >
                    </el-descriptions-item>
                  </el-descriptions>
                </div>
              </div>
            </div>
          </div>
        </div>
      </el-card>
    </div>
  </div>

  <!-- 支付窗口 -->
  <el-dialog v-model="payDialog" title="支付订单" width="500" class="dialog">
    <span>需要支付金额：{{ toHandleOrderItem.total }}</span>
    <el-input v-model="payPrice" placeholder="请输入支付金额"></el-input>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="payDialog = false" round>取消</el-button>
        <el-button type="primary" @click="handlePay" round> 支付 </el-button>
      </div>
    </template>
  </el-dialog>

  <!-- 签收窗口 -->
  <el-dialog v-model="signDialog" title="签收订单" width="500" class="dialog">
    <span>确认签收？</span>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="signDialog = false" round>取消</el-button>
        <el-button type="primary" @click="handleSign" round> 签收 </el-button>
      </div>
    </template>
  </el-dialog>

  <!-- 评价窗口 -->
  <el-dialog
    v-model="commentDialog"
    title="评价订单"
    width="500"
    class="dialog"
  >
    <span>输入评价</span>
    <el-input
      v-model="comment"
      placeholder="评价一旦发布就不能修改哦！"
    ></el-input>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="commentDialog = false" round>取消</el-button>
        <el-button type="primary" @click="handleComment" round>
          评价
        </el-button>
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
  deleteSingleOrderApi as deleteSingleOrder,
  changeOrderStatusApi as changeOrderStatus,
  commentOrderApi as commentOrder
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

const getOrdersProfile = () => {
  return getOrders({
    token: localStorage.getItem('TOKEN')
  })
    .then((res: any) => {
      OrdersProfile.data = res.data.data
      console.log(res)
    })
    .catch((err: any) => {
      console.log(err)
    })
}

// 加载页面时候获取购物车物品详细数据
onMounted(async () => {
  try {
    await getOrdersProfile()
  } catch (error) {
    console.error(error)
  }
})

// 订单状态修改
const payDialog = ref(false)
const toHandleOrderItem = reactive({ total: '', data: {} })
const payPrice = ref()
const signDialog = ref(false)
const changeStatus = (item: any, index: any) => {
  if (item.status_name === '待支付') {
    // 支付
    toHandleOrderItem.data = item
    toHandleOrderItem.total = (
      parseInt(toHandleOrderItem.data.quantity) *
      parseFloat(toHandleOrderItem.data.price)
    ).toString()
    // console.log(toHandleOrderItem.data)
    payDialog.value = true
  } else if (item.status_name === '已送达') {
    // 签收
    toHandleOrderItem.data = item
    signDialog.value = true
  } else if (item.status_name === '已签收') {
    // 评价
    toHandleOrderItem.data = item
    commentDialog.value = true
  } else {
    // 剩余不变
  }
}

// 删除订单
const deleteOrder = (orderId: any) => {
  return deleteSingleOrder(orderId)
    .then((res) => {
      getOrdersProfile()
      console.log(res)
    })
    .catch((err) => {
      console.log(err)
    })
}

const handlePay = () => {
  if (toHandleOrderItem.total === payPrice.value) {
    ElMessage.success('成功支付！待商家发货！')
    // 提起订单状态更改请求
    changeOrderStatus({
      orderItemId: toHandleOrderItem.data.orderdetail_id,
      newStatus: 'pending'
    })
      .then((res: any) => {
        console.log(res)
      })
      .catch((err: any) => {
        console.log(err)
      })
  } else ElMessage.error('支付金额错误！')
  payDialog.value = false
}

const handleSign = () => {
  // 提起订单状态更改请求
  changeOrderStatus({
    orderItemId: toHandleOrderItem.data.orderdetail_id,
    newStatus: 'confirmed'
  })
    .then((res) => {
      console.log(res)
    })
    .catch((err) => {
      console.log(err)
    })
  signDialog.value = false
}

// 评价订单
const commentDialog = ref(false)
const comment = ref('')
const handleComment = () => {
  // 提起订单状态更改请求
  commentOrder({
    orderItemId: toHandleOrderItem.data.orderdetail_id,
    comment: comment.value
  })
    .then((res: any) => {
      console.log(res)
    })
    .catch((err: any) => {
      console.log(err)
    })
  commentDialog.value = false
}
</script>
<script lang="ts">
export default {}
</script>

<style lang="less" scoped>
@import '@/assets/styles/common.css';
.MyOrder {
  min-height: 100%;
  margin: 0;
  background-color: #f0f0f0;

  .Container {
    padding: 15px;
    .MyOrderPanel {
      border-radius: 25px;
      padding: 20px;
      .backButton {
        float: left;
      }

      .MyOrderContent {
        .MyOrderInfo {
          margin-bottom: 10px;
          padding: 10px;
        }

        .MyOrderUnit {
          background: #eaeaea;
          margin-bottom: 20px;
          padding: 10px;
          border: 1px solid #e7e7e7;
          border-radius: 25px;

          .OrderProfile {
            background-color: #ffffff;
            padding: 10px;
            border-radius: 25px;
          }

          .OrderItemsBox {
            background: #ffffff;
            padding: 10px;
            border-radius: 25px;
            border: 1px solid #e7e7e7;
            margin-top: 10px;

            .OrderItemsUnit {
              display: flex;
              margin: 5px 0;
              padding: 10px;
              border-radius: 25px;
              border: 1px solid #e7e7e7;

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
      }

      .settleButton {
        float: right;
      }
    }
  }
}
</style>
