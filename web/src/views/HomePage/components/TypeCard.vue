<template>
  <div class="TypeCard">
    <el-card class="Card">
      <template #header><span class="CardHeader">商品种类</span></template>
      <div class="TypeContent">
        <el-row>
          <el-col
            :span="4"
            class="TypeUnit"
            v-for="item in GoodsProfile.typeRoad"
            :key="item.id"
            @click="toGoodsPage('goods', item.id)"
          >
            {{ item.item_type }}
          </el-col>
          <el-divider />
          <el-col
            :span="4"
            class="TypeUnit"
            v-for="item in GoodsProfile.typeHill"
            :key="item.id"
            @click="toGoodsPage('goods', item.id)"
          >
            {{ item.item_type }}
          </el-col>
        </el-row>
      </div>
      <template #footer
        ><span class="CardFooter" @click="toPage('goods')"
          >了解更多</span
        ></template
      >
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, reactive } from 'vue'
import { getItemTypesByBikeApi as ItemTypesByBike } from '@/apis/item'
import { useRouter } from 'vue-router'

const GoodsProfile = reactive({
  typeRoad: [],
  typeHill: []
})
const router = useRouter()
const toPage = (param: string) => {
  const name = param.toString()
  router.push({ name: name })
}

const toGoodsPage = (param: string, itemTypeId: any) => {
  const name = param.toString()
  router.push({ name: name, query: { itemTypeId: itemTypeId } })
}

// 获取全部商品分类
const getItemType = (bikeType: string) => {
  ItemTypesByBike({ bikeType: bikeType })
    .then((res: any) => {
      if (bikeType === 'Road') {
        GoodsProfile.typeRoad = res.data.data
      } else if (bikeType === 'Hill') GoodsProfile.typeHill = res.data.data
    })
    .catch((err) => {
      console.error(err)
      throw err
    })
}

onMounted(async () => {
  try {
    await getItemType('Road')
    await getItemType('Hill')
  } catch (error) {
    console.error(error)
  }
})
</script>
<script lang="ts">
export default {
  name: 'TypeCard'
}
</script>

<style lang="less" scoped>
.TypeCard {
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

  .TypeContent {
    .TypeUnit {
      margin: 5px auto;
      padding: 5px 10px;
      line-height: 25px;
      transition: all 0.1s linear;
    }

    .TypeUnit:hover {
      background: #85c1bf;
      color: #ffffff;
      border-radius: 25px;
      transform: scale(1.1);
    }
  }
  .CardFooter {
    display: block;
    text-align: right;
  }

  .TypeContent {
  }
}
</style>
