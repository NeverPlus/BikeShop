<template>
  <div class="DiyTab">
    <el-container>
      <!-- 分类 -->
      <el-aside style="padding: 10px" width="200px">
        <el-card class="TypesPanel">
          <template #header>自组模式</template>
          <el-radio-group
            v-model="activeMode"
            size="large"
            style="display: flex"
          >
            <div class="typeTag">
              <el-radio-button label="严格模式" value="Strict" />
            </div>
            <div class="typeTag">
              <el-radio-button label="零件模式" value="Parts" />
            </div>
            <div class="typeTag">
              <el-radio-button label="自行车整车" value="Bike" />
            </div>
          </el-radio-group>
        </el-card>
      </el-aside>
      <!-- 组装面板 -->
      <el-main style="padding: 10px">
        <el-card class="DiyPanel">
          <template #header>DIY面板</template>
          <!-- 自行车图片 -->
          <div class="BikeImg">
            <img
              v-if="bikeType === 'Road'"
              src="@/assets/images/RoadBike.jpg"
              alt=""
              width="100%"
            />
            <img
              v-else
              src="@/assets/images/HillBike.jpg"
              alt=""
              width="100%"
            />
          </div>
          <!-- 选择自行车部件 -->
          <!-- 如果是自组 -->
          <div v-if="activeMode.valueOf() != 'Bike'" class="SelectParts">
            <el-row>
              <el-col
                :span="12"
                v-for="(type, index) in GoodsProfile.typeData"
                :key="index"
              >
                <el-card class="PartsUnit">
                  <template #header>
                    <div class="card-header">
                      <span>{{ type.item_type }}</span>
                    </div>
                  </template>
                  <el-container>
                    <el-main>
                      <el-empty
                        v-if="GoodsProfile.typeItems[index].num <= 0"
                        :image-size="100"
                        description="还没有选择部件！"
                        style="height: 125px"
                      />
                      <div v-else class="GoodsUnit">
                        <div class="GoodsImg">
                          <el-image
                            :src="
                              baseURL +
                              GoodsProfile.typeItems[index].data.item_image
                            "
                            style="height: 100%"
                            fit="scale-down"
                          />
                        </div>
                        <div class="GoodsDesc">
                          <el-text class="GoodsName">{{
                            GoodsProfile.typeItems[index].data.item_name
                          }}</el-text>
                          <el-text class="GoodsNum"
                            >数量：{{
                              GoodsProfile.typeItems[index].num
                            }}</el-text
                          >
                          <div class="GoodsSale">
                            <el-text class="GoodsPrice"
                              >￥{{
                                GoodsProfile.typeItems[index].data.price
                              }}</el-text
                            >
                          </div>
                        </div>
                      </div>
                    </el-main>
                    <el-aside width="100px">
                      <el-button
                        class="PartsButton"
                        type="primary"
                        round
                        @click="loadTpyeItems(type.id)"
                        >选择部件</el-button
                      >
                      <el-button
                        class="PartsButton"
                        type="danger"
                        round
                        @click="deleteTpyeItems(index)"
                        >删除部件</el-button
                      >
                    </el-aside>
                  </el-container>
                </el-card>
              </el-col>
            </el-row>
          </div>
          <!-- 如果选择整车 -->
          <div v-else class="SelectBikes">
            <el-empty
              description="该分类下暂时没有商品！"
              v-if="Object.keys(GoodsProfile.bikeData).length === 0"
            />
            <el-row v-else>
              <el-col
                :span="6"
                v-for="item in GoodsProfile.bikeData"
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
                        >{{ item.item_status ? '购买' : '售罄' }}</el-button
                      >
                    </div>
                  </div>
                </div>
              </el-col>
            </el-row>
          </div>
          <template #footer>
            <el-button type="primary" round @click="summitParts"
              >提交</el-button
            >
            <el-button type="danger" round @click="clearParts">清空</el-button>
          </template>
        </el-card>
      </el-main>
    </el-container>
  </div>

  <!-- 弹出选择某类部件窗口 -->
  <el-dialog
    class="dialog"
    v-model="dialogPartsVisible"
    title="选择部件"
    width="1000"
  >
    <DiyTabDialog :typeId="selectedType.id" @selected-item="getSelectedItem" />
  </el-dialog>
</template>

<script lang="ts" setup>
import { onMounted, reactive, defineProps, ref } from 'vue'
import DiyTabDialog from './DiyTabDialog.vue'
import baseURL from '@/utils/axios'
import {
  getItemTypesByBikeApi as ItemTypesByBike,
  getBikesByBikeApi as getBikesByBike
} from '@/apis/item'
import { addCartItemsApi as addItemsToCart } from '@/apis/cart'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

// 接收参数
const props = defineProps({
  bikeType: String
})

// 选择组装的模式
const activeMode = ref('Strict')

const GoodsProfile = reactive({
  typeData: [],
  typeItems: [],
  bikeData: []
})

const router = useRouter()
const toItemDetail = (params: any) => {
  const itemId = params.toString()
  router.push({ name: 'item_detail', query: { itemId: itemId } })
}

// 获取部件种类
const getItemType = (bikeType: any) => {
  return ItemTypesByBike({ bikeType: bikeType })
    .then((res: any) => {
      GoodsProfile.typeData = res.data.data
      GoodsProfile.typeData.forEach((element) => {
        GoodsProfile.typeItems.push({
          id: element.id,
          name: element.item_type,
          data: {},
          num: 0
        })
      })
    })
    .catch((err) => {
      console.error(err)
      throw err
    })
}
// 获取整车数据
const getBikesProfileByBike = (bikeType: any) => {
  return getBikesByBike({ bikeType: bikeType })
    .then((res: any) => {
      GoodsProfile.bikeData = res.data.data
    })
    .catch((err) => {
      console.error(err)
      throw err
    })
}

onMounted(async () => {
  try {
    await getItemType(props.bikeType)
    await getBikesProfileByBike(props.bikeType)
  } catch (error) {
    console.error(error)
  }
})
// 对话框相关
const dialogPartsVisible = ref(false)
const selectedType = reactive({ id: '' })

// 进入对话框部件之前处理信息
const loadTpyeItems = (typeId: any) => {
  // 获取同种部件的所有部件信息
  selectedType.id = typeId.toString()
  dialogPartsVisible.value = true
}

// 选择之后关闭对话框并获取数据
const deleteTpyeItems = (index: any) => {
  // 获取同种部件的所有部件信息
  GoodsProfile.typeItems[index].data = {}
  GoodsProfile.typeItems[index].num = 0
}

// 获取选择的部件
const getSelectedItem = (selectedItem: any) => {
  // 找到对应的typeItems的序号
  const index = GoodsProfile.typeItems.findIndex(
    (type) => type.name === selectedItem.data.item_type
  )

  // 注入数据
  GoodsProfile.typeItems[index].data = selectedItem.data
  GoodsProfile.typeItems[index].num = selectedItem.num
  dialogPartsVisible.value = false
}

// 提交到购物车
const summitParts = () => {
  const toCartItems = [] as any
  if (activeMode.value === 'Strict') {
    for (let index = 0; index < GoodsProfile.typeItems.length; index++) {
      if (
        GoodsProfile.typeItems[index].num === 0 &&
        GoodsProfile.typeItems[index].name !== '其他'
      ) {
        return ElMessage.error('还有零件没有选择')
      }
    }
    return ElMessage.success('提交成功')
  } else if (activeMode.value === 'Parts') {
    GoodsProfile.typeItems.forEach((element) => {
      if (element.num !== 0) {
        toCartItems.push({
          itemId: element.data.item_id,
          quantity: element.num
        })
      }
    })
    addItemsToCart({ token: localStorage.getItem('TOKEN'), items: toCartItems })
      .then()
      .catch()
    return ElMessage.success('提交零件成功')
  } else {
    return ElMessage.success('提交整车成功')
  }
}
// 清空
const clearParts = () => {
  GoodsProfile.typeItems.forEach((element) => {
    element.data = {}
    element.num = 0
  })
  ElMessage.success('清空成功')
}
</script>

<script lang="ts">
export default {
  name: 'DiyTab'
}
</script>

<style lang="less" scoped>
.DiyTab {
  .TypesPanel {
    border-radius: 25px;
    .typeTag {
      border-radius: 25px;
      background-color: #b4b4b4;
      margin: 5px auto;
      width: auto;
    }
  }

  .DiyPanel {
    border-radius: 25px;

    .BikeImg {
      border: 1px solid #e7e7e7;
      border-radius: 25px;
      overflow: hidden;
    }

    .SelectParts {
      .PartsUnit {
        height: 250px;
        margin: 10px;
        border-radius: 25px;

        .GoodsUnit {
          display: flex;
          padding: 15px;
          border-radius: 25px;
          box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.218);
          overflow: hidden;

          .GoodsImg {
            display: inline-block;
            height: 100px;
            width: 100px;
            border: 1px solid #e7e7e7;
            border-radius: 25px;
            overflow: hidden;
          }

          .GoodsDesc {
            padding-left: 10px;
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
            .GoodsNum {
              display: flex;
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

        .PartsButton {
          margin: 10px 0;
        }

        /deep/ .el-card__body {
          padding: 5px;
        }
      }
    }

    .SelectBikes {
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
            font-size: 25px;
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
</style>
