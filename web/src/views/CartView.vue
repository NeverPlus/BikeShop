<template>
  <div class="Cart">
    <div class="Container">
      <el-card class="CartPanel">
        <template #header>
          <el-button class="backButton" type="default" round @click="backPage"
            ><el-icon class="MyNavUnitIcon"><ArrowLeft /></el-icon
            >返回</el-button
          >
          <span class="CardHeader">购物车</span></template
        >
        <el-empty
          v-if="Object.keys(CartProfile.data).length === 0"
          description="购物车空空如也！"
        />
        <div v-else class="CartContent">
          <div
            class="CartUnit"
            v-for="(item, index) in CartProfile.data"
            :key="index"
          >
            <el-checkbox
              class="itemCheck"
              v-model="item.check"
              @change="checkItem(index)"
            />
            <div class="itemImg">
              <img :src="baseURL + item.item_image" alt="" height="100%" />
            </div>
            <div class="itemProfile">
              <el-descriptions :title="item.item_name">
                <el-descriptions-item label="商品种类:">{{
                  item.item_type
                }}</el-descriptions-item>
                <el-descriptions-item label="数量:">
                  <el-input-number
                    v-model="CartProfile.data[index].quantity"
                    :min="1"
                    :max="item.item_quantity"
                    @change="editItem(index)"
                  />
                </el-descriptions-item>
                <el-descriptions-item label="价格:">{{
                  item.price
                }}</el-descriptions-item>
              </el-descriptions>
            </div>
            <div class="itemAction">
              <el-button
                round
                type="danger"
                @click="confirmDelete(item.cartdetail_id)"
                >删除</el-button
              >
            </div>
          </div>
        </div>
        <template #footer>
          <span class="CardFooter">总价：￥{{ CartProfile.total.toFixed(2) }}</span>
          <el-checkbox
            class="itemAllCheck"
            label="全选"
            v-model="checkAll"
            @change="checkAllItem()"
            style="float: left"
          />
          <el-button
            class="settleButton"
            type="primary"
            round
            @click="submitOrder"
          >
            结算
          </el-button>
        </template>
      </el-card>
    </div>

    <!-- 确认删除 -->
    <el-dialog
      class="dialog"
      v-model="deleteCartItemDialog"
      title="Tips"
      width="500"
    >
      <span>确认删除？</span>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="cancelDelete" round>取消</el-button>
          <el-button type="danger" @click="deleteCart" round> 删除 </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft } from '@element-plus/icons-vue'
import baseURL from '@/utils/axios'
import {
  getCartItemApi as getCart,
  editCartItemApi as editCartItem,
  deleteCartItemApi as deletCartItem
} from '@/apis/cart'
import { orderItemsApi as orderItems } from '@/apis/order'

const router = useRouter()
const route = useRoute()
const CartProfile = reactive({ data: [], total: 0 })

// 进入购物车页面需要获取该购物车所对应的用户id
// const userId = route.query.userId

// 返回键的操作
const backPage = () => {
  router.back()
}

const toPage = (param: string) => {
  const name = param.toString()
  router.push({ name: name })
}

// 发起请求获取购物车数据
const getCartProfile = () => {
  return getCart({ token: localStorage.getItem('TOKEN') })
    .then((res: any) => {
      const result = res.data.data
      result.forEach((element: any) => {
        CartProfile.data.push({ ...element, check: false })
      })
      console.log(CartProfile.data)

      CartProfile.total = 0
    })
    .catch((err: any) => {
      console.log(err)
    })
}

// 加载页面时候获取购物车物品详细数据
onMounted(async () => {
  try {
    await getCartProfile()
  } catch (error) {
    console.error(error)
  }
})

// 购物车计算总价
// 选择一个
const checkItem = (index: any) => {
  CartProfile.total = 0
  CartProfile.data.forEach((element: any) => {
    if (element.check) {
      CartProfile.total =
        CartProfile.total +
        parseFloat(element.price) * parseInt(element.quantity)
    }
  })
}
// 全选
const checkAll = ref(false)
const checkAllItem = () => {
  CartProfile.data.forEach((element: any) => {
    element.check = checkAll.value
    CartProfile.total =
      CartProfile.total + parseFloat(element.price) * parseInt(element.quantity)
  })
  if (!checkAll.value) {
    CartProfile.total = 0
  }
}

// 修改购物车内物品参数
const editItem = async (index: any) => {
  return editCartItem({
    token: localStorage.getItem('TOKEN'),
    ...CartProfile.data[index]
  })
    .then((res: any) => {
      // 同步获取到的数据、总价和数字输入框的数据
      // CartProfile.total = res.data.total
      if (res.code === 200) {
        console.log(res)
      }
    })
    .catch((err) => {
      console.log(err)
    })
}

// 删除购物车内物品
const deleteCartItemDialog = ref(false)
const itemToDelete = ref()
const confirmDelete = (itemId: any) => {
  itemToDelete.value = itemId
  deleteCartItemDialog.value = true
}

const cancelDelete = () => {
  itemToDelete.value = null
  deleteCartItemDialog.value = false
}

const deleteCart = () => {
  deleteCartItemDialog.value = false
  return deletCartItem({
    token: localStorage.getItem('TOKEN'),
    cartdetail_id: parseInt(itemToDelete.value)
  })
    .then((res) => {
      CartProfile.data = []
      getCartProfile()
      console.log(res)
    })
    .catch((err) => {
      console.log(err)
    })
}

// 提交购物车表单生成订单
const submitOrder = () => {
  const OrderItem = [] as any
  CartProfile.data.forEach((element: any) => {
    if (element.check) {
      OrderItem.push(element.cartdetail_id)
    }
  })
  router.push({ name: 'order', query: { itemsId: OrderItem, type: 'cart' } })
}
</script>
<script lang="ts">
export default {}
</script>

<style lang="less" scoped>
@import '@/assets/styles/common.css';
.Cart {
  min-height: 100%;
  margin: 0;
  background-color: #f0f0f0;

  .Container {
    padding: 15px;
    .CartPanel {
      border-radius: 25px;
      padding: 20px;
      .backButton {
        float: left;
      }

      .CartContent {
        .CartUnit {
          display: flex;
          margin-bottom: 10px;
          padding: 10px;
          border: 1px solid #e7e7e7;
          border-radius: 25px;
          .itemCheck {
            display: inline-block;
            margin: auto 0;
            padding: 5px;
          }

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
