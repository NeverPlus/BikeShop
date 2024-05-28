<template>
  <div class="DiyTabDialog">
    <el-card class="ItemsPanel">
      <el-empty
        v-if="GoodsProfile.typeItems.length == 0"
        description="还没有部件！"
      />
      <el-row v-else>
        <el-col
          :span="6"
          v-for="item in GoodsProfile.typeItems"
          :key="item.item_id"
        >
          <div class="ItemUnit">
            <div class="ItemImg" @click="toItemDetail(item.item_id)">
              <el-image
                :src="baseURL + item.item_image"
                style="height: 100%"
                fit="scale-down"
              />
            </div>
            <div class="ItemDesc">
              <el-text class="ItemName">{{ item.item_name }}</el-text>
              <el-text class="ItemNum">
                <el-input-number
                  v-model="GoodsProfile.selectedItem.num"
                  :min="1"
                  :max="item.item_quantity"
                />
              </el-text>
              <div class="ItemSale">
                <el-text class="ItemPrice">￥{{ item.price }}</el-text>
                <el-button
                  class="ItemBuy"
                  type="primary"
                  round
                  @click="selectTpyeItems(item)"
                  :disabled="item.item_status ? false : true"
                  >{{ item.item_status ? '选择' : '售罄' }}</el-button
                >
              </div>
            </div>
          </div>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { reactive, defineProps, ref, watch, defineEmits } from 'vue'
import { getItemsByTypeApi as getItemsByType } from '@/apis/item'
import baseURL from '@/utils/axios'
import { useRouter } from 'vue-router'

// 接收参数
const props = defineProps({
  typeId: String
})

// 返回数据
const emit = defineEmits(['selectedItem'])

const GoodsProfile = reactive({
  typeItems: [],
  selectedItem: { data: {}, num: 0 }
})

const getItemsProfileByType = (typeId: any) => {
  return getItemsByType({ typeId: typeId })
    .then((res: any) => {
      GoodsProfile.typeItems = res.data.data
    })
    .catch((err) => {
      console.error(err)
      throw err
    })
}

// 实时更新组件信息
watch(
  () => props.typeId,
  (newValue, oldValue) => {
    getItemsProfileByType(newValue)
  }
)

// 点击按钮返回选择的商品id和数量
const selectTpyeItems = (item: any) => {
  GoodsProfile.selectedItem.data = item
  emit('selectedItem', GoodsProfile.selectedItem)
}

const router = useRouter()
const toItemDetail = (params: any) => {
  const itemId = params.toString()
  const url = router.resolve({ name: 'item_detail', query: { itemId: itemId } })
  window.open(url.href)
}
</script>
<script lang="ts">
export default {
  name: 'DiyTabDialog'
}
</script>

<style lang="less" scoped>
.DiyTabDialog {
  .ItemsPanel {
    border-radius: 25px;

    .ItemUnit {
      // flex: 1;
      display: inline-block;
      margin: 10px;
      padding: 15px;
      border-radius: 25px;
      box-shadow: 0 0 5px rgba(0, 0, 0, 0.218);
      overflow: hidden;

      .ItemImg {
        height: 150px;
        width: 150px;
        border: 1px solid #e7e7e7;
        border-radius: 25px;
        overflow: hidden;
      }

      .ItemDesc {
        .ItemName {
          display: block;
          padding: 5px 5px;
          width: 140px;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
          font-size: 20px;
          text-align: left;
        }
        .ItemNum {
          display: block;
          padding: 2px 5px;
          font-size: 15px;
          text-align: left;
        }
        .ItemSale {
          display: flex;
          padding: 5px;
          .ItemPrice {
            display: inline-block;
            flex: 4;
            text-align: left;
          }
          .ItemBuy {
            display: inline-block;
            flex: 1;
          }
        }
      }
    }
  }
}
</style>
