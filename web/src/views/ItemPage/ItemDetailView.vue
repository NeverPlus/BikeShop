<template>
  <div class="ItemDetail">
    <div class="Container">
      <el-card class="ItemDetailPanel">
        <template #header
          ><el-button class="backButton" type="default" round @click="backPage"
            ><el-icon class="MyNavUnitIcon"><ArrowLeft /></el-icon
            >返回</el-button
          >
          <span class="CardHeader">商品详情</span>
        </template>
        <!-- 商品内容 -->
        <div class="itemContent">
          <!-- 商品图片 -->
          <div class="itemImage">
            <el-image
              :src="baseURL + itemProfile.data.item_image"
              alt=""
              fit="contain"
            />
          </div>
          <!-- 商品名字和选择规格 -->
          <div class="itemSpec">
            <div class="itemDesc">
              <el-text class="itemText itemName">{{
                itemProfile.data.item_name
              }}</el-text>
              <el-text class="itemText itemType">
                商品种类：{{ itemProfile.data.item_type }}</el-text
              >
              <el-text class="itemText itemType">
                商家：{{ itemProfile.data.merchant }}</el-text
              >
              <el-text class="itemText itemPrice"
                >￥{{ itemProfile.data.price }}</el-text
              >
            </div>
            <el-form ref="formRef" :model="form" style="max-width: 600px">
              <!-- 商品数量 -->
              <el-form-item label="数量：" prop="quantity">
                <el-input-number
                  v-model="form.quantity"
                  :min="1"
                  :max="itemProfile.data.item_quantity"
                />
              </el-form-item>
              <el-form-item>
                <el-button
                  type="primary"
                  @click="submitBuyForm(itemProfile.data.item_id)"
                  :disabled="itemProfile.data.item_status ? false : true"
                  round
                  >{{
                    itemProfile.data.item_status ? '购买' : '售罄'
                  }}</el-button
                >
                <el-button type="success" @click="submitCartForm()" round
                  >加入购物车</el-button
                >
              </el-form-item>
            </el-form>
          </div>
        </div>
        <el-tabs v-model="activeName" class="itemDesc">
          <el-tab-pane label="商品描述" name="desc">
            <el-empty
              v-if="itemProfile.data.item_desc.length <= 0"
              description="该商品暂时没有详细介绍！"
            />
            <div
              v-else
              class="itemDescImgs"
              v-for="(image, index) in itemProfile.data.item_desc"
              :key="index"
            >
              <img :src="baseURL + image" width="100%" alt="" />
            </div>
          </el-tab-pane>
        </el-tabs>
      </el-card>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, reactive, ref } from 'vue'
import { ElMessage, FormInstance } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import baseURL from '@/utils/axios'
import { getItemApi as getItem } from '@/apis/item'
import { addCartItemApi as addItemToCart } from '@/apis/cart'
import { useRoute, useRouter } from 'vue-router'
const router = useRouter()
const route = useRoute()
const itemId = route.query.itemId
const itemProfile = reactive({ data: { item_desc: [] } })
const activeName = ref('desc')

const backPage = () => {
  router.back()
}

const getItemProfile = () => {
  return getItem({ itemId: itemId })
    .then((res: any) => {
      if (res.code === 200) {
        itemProfile.data = res.data.data
        console.log(itemProfile.data)
      }
    })
    .catch((err) => {
      console.error(err)
      throw err
    })
}

onMounted(async () => {
  try {
    await getItemProfile()
    form.itemId = itemId.toString()
  } catch (error) {
    console.error(error)
  }
})

const formRef = ref<FormInstance>()
const form = reactive({
  itemId: '',
  quantity: 1
})

// 买商品
const submitBuyForm = (itemId: any) => {
  if (!formRef.value) return
  formRef.value.validate((valid) => {
    if (valid) {
      // 递送数据到确认订单
      router.push({
        name: 'order',
        query: { itemsId: form.itemId, quantity: form.quantity, type: 'direct' }
      })
    }
  })
}

// 加入购物车
const submitCartForm = () => {
  if (!formRef.value) return
  formRef.value.validate((valid) => {
    if (valid) {
      console.log(form)

      // 提交更新
      addItemToCart({ token: localStorage.getItem('TOKEN'), ...form })
        .then((res: any) => {
          ElMessage.success('添加到购物车成功！')
          console.log(res)
        })
        .catch((err: any) => {
          console.log(err)
        })
    }
  })
}
</script>

<script lang="ts">
export default {
  name: 'itemDetail'
}
</script>

<style lang="less" scoped>
@import '@/assets/styles/common.css';
.ItemDetail {
  min-height: 100%;
  margin: 0;
  background-color: #f0f0f0;

  .Container {
    padding: 15px;
    .ItemDetailPanel {
      border-radius: 25px;
      padding: 20px;
      .backButton {
        float: left;
      }

      .itemContent {
        display: flex;
        .itemImage {
          display: inline-block;
          border-radius: 25px;
          overflow: hidden;
          width: 350px;
          height: 350px;
        }

        .itemSpec {
          padding: 15px;
          .itemText {
            display: block;
            text-align: left;
            padding: 10px 0;
          }

          .itemName {
            font-size: 40px;
            font-weight: 700;
          }

          .itemType {
            font-size: 15px;
            font-weight: 100;
          }

          .itemPrice {
            font-size: 25px;
            font-weight: 200;
            color: #4d91ff;
          }
        }

        el-form > el-form-item {
          margin: auto;
        }
      }

      .itemDesc {
      }
    }
  }
}
</style>
