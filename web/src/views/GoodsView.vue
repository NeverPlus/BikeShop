<template>
  <div class="Goods">
    <div class="Container">
      <el-card class="GoodsPanel">
        <el-container>
          <!-- 分类 -->
          <el-aside style="padding: 10px" width="200px"
            ><el-card class="TypesPanel">
              <!-- 公路车山地车零件分类 -->
              <el-tabs v-model="activeType" class="TypesTabs">
                <el-tab-pane label="公路车" name="Road">
                  <div
                    class="typeTag"
                    v-for="(type, index) in GoodsProfile.typeRoad"
                    :key="index"
                    @click="getItemsProfileByType(type.id)"
                  >
                    {{ type.item_type }}
                  </div>
                </el-tab-pane>
                <el-tab-pane label="山地车" name="Hill">
                  <div
                    class="typeTag"
                    v-for="(type, index) in GoodsProfile.typeHill"
                    :key="index"
                    @click="getItemsProfileByType(type.id)"
                  >
                    {{ type.item_type }}
                  </div>
                </el-tab-pane>
              </el-tabs>
            </el-card>
          </el-aside>
          <!-- 商品列表 -->
          <el-main style="padding: 10px"
            ><el-card class="ItemsPanel">
              <template #header>商品列表</template>
              <el-empty
                description="该分类下暂时没有商品！"
                v-if="Object.keys(GoodsProfile.typeItems).length === 0"
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
                      <el-text class="ItemType">{{ item.item_type }}</el-text>
                      <div class="ItemSale">
                        <el-text class="ItemPrice">￥{{ item.price }}</el-text>
                        <el-button
                          class="ItemBuy"
                          type="primary"
                          round
                          :disabled="item.item_status ? false : true"
                          @click="toItemDetail(item.item_id)"
                          >{{ item.item_status ? '购买' : '售罄' }}</el-button
                        >
                      </div>
                    </div>
                  </div>
                </el-col>
              </el-row>
            </el-card>
          </el-main>
        </el-container>
      </el-card>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import baseURL from '@/utils/axios'
import {
  getItemTypesByBikeApi as ItemTypesByBike,
  getItemsByTypeApi as getItemsByType
} from '@/apis/item'

// 如果跳转过来有参数
const route = useRoute()
const itemTypeId = parseInt(route.query.itemTypeId as string)

// 选择哪种自行车零件
const activeType = ref('Road')

const GoodsProfile = reactive({
  typeRoad: [],
  typeHill: [],
  typeItems: []
})

const toItemDetail = (params: any) => {
  const itemId = params.toString()
  router.push({ name: 'item_detail', query: { itemId: itemId } })
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

// 获取分类下所有商品
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

const router = useRouter()

onMounted(async () => {
  try {
    await getItemType('Road')
    await getItemType('Hill')
    await getItemsProfileByType(itemTypeId)
  } catch (error) {
    console.error(error)
  }
})
</script>
<script lang="ts">
export default {}
</script>

<style lang="less" scoped>
@import '@/assets/styles/common.css';
.Goods {
  min-height: 100%;
  margin: 0;
  background-color: #f0f0f0;

  .Container {
    padding: 15px;
    .GoodsPanel {
      border-radius: 25px;

      .TypesPanel {
        border-radius: 25px;
        .typeTag {
          border-radius: 25px;
          background-color: #cacaca;
          margin: 5px 0;
          padding: 10px;
          line-height: 40px;
          transition: all 0.1s linear;
        }

        .typeTag:hover {
          border-radius: 25px;
          color: #ffffff;
          background-color: #85c1bf;
          transform: scale(1.05);
        }
      }

      .ItemsPanel {
        border-radius: 25px;

        .ItemUnit {
          // flex: 1;
          display: inline-block;
          margin: 10px;
          padding: 15px;
          border-radius: 25px;
          box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.218);
          overflow: hidden;
          transition: all 0.1s linear;

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
            .ItemType {
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

        .ItemUnit:hover {
          transform: scale(1.05);
        }
      }
    }
  }
}
</style>
