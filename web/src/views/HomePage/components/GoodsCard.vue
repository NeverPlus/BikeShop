<template>
  <div class="GoodsCard">
    <el-card class="Card">
      <template #header
        ><span class="CardHeader">{{ title }}</span></template
      >
      <el-empty
        description="暂时没有商品！"
        v-if="Object.keys(itemsProfile.data).length === 0"
      />
      <div
        v-else
        class="GoodsUnit"
        v-for="item in itemsProfile.data"
        :key="item.item_id"
      >
        <div class="GoodsImg" @click="toItemDetail(item.item_id)">
          <el-image
            :src="baseURL + item.item_image"
            style="height: 100%"
            fit="scale-down"
          />
        </div>
        <div class="GoodsDesc">
          <el-text class="GoodsName">{{ item.item_name }}</el-text>
          <el-text class="GoodsType">{{ item.item_type }}</el-text>
          <div class="GoodsSale">
            <el-text class="GoodsPrice">￥{{ item.price }}</el-text>
            <el-button
              class="GoodsBuy"
              type="primary"
              round
              @click="toItemDetail(item.item_id)"
              :disabled="item.item_status ? false : true"
              >{{ item.item_status ? '购买' : '售罄' }}
            </el-button>
          </div>
        </div>
      </div>
      <template #footer
        ><span class="CardFooter" @click="toPage('diy')"
          >了解更多</span
        ></template
      >
    </el-card>
  </div>
</template>

<style lang="less" scoped>
.GoodsCard {
  //   display: flex;
  margin-bottom: 10px;

  .Card {
    border-radius: 25px;
  }

  .CardHeader {
    display: block;
    text-align: center;
    line-height: 200%;
    border-radius: 10px;
    background: #bad5ff;
    width: 100px;
  }
  .CardFooter {
    display: block;
    text-align: right;
  }

  .GoodsUnit {
    // flex: 1;
    display: inline-block;
    margin: 10px;
    padding: 15px;
    border-radius: 25px;
    box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.218);
    overflow: hidden;
    transition: all 0.2s linear;

    .GoodsImg {
      height: 150px;
      width: 150px;
      border: 1px solid #e7e7e7;
      border-radius: 25px;
      overflow: hidden;
    }

    .GoodsDesc {
      .GoodsName {
        display: block;
        padding: 5px 5px;
        width: 140px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        font-size: 20px;
        text-align: left;
      }
      .GoodsType {
        display: block;
        padding: 2px 5px;
        font-size: 15px;
        text-align: left;
      }
      .GoodsSale {
        display: flex;
        padding: 5px;
        .GoodsPrice {
          display: inline-block;
          flex: 4;
          text-align: left;
        }
        .GoodsBuy {
          display: inline-block;
          flex: 1;
        }
      }
    }
  }

  .GoodsUnit:hover {
    transform: scale(1.05);
  }
}
</style>

<script lang="ts" setup>
import { onMounted, reactive, defineProps } from 'vue'
import baseURL from '@/utils/axios'
import { getRecommendItemApi as getRecommendItem } from '@/apis/item'
import { useRouter } from 'vue-router'

// 接收参数
const props = defineProps({
  title: String,
  type: String
})

const itemsProfile = reactive({ data: [] })
const router = useRouter()
const toPage = (param: string) => {
  const name = param.toString()
  router.push({ name: name })
}

// 获取商品图数据（预插入）
onMounted(async () => {
  try {
    await getRecommendItem({ type: props.type })
      .then((res: any) => {
        itemsProfile.data = res.data.data
        console.log(itemsProfile.data)
      })
      .catch((err) => {
        console.log(err)
      })
  } catch (error) {
    console.error(error)
  }
})

const toItemDetail = (params: any) => {
  const itemId = params.toString()
  router.push({ name: 'item_detail', query: { itemId: itemId } })
}
</script>
<script lang="ts">
export default {
  name: 'GoodsCard'
}
</script>
