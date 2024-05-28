<template>
  <div class="Search">
    <div class="Container">
      <!-- 搜索栏 -->
      <div class="SearchBar">
        <div class="ShopTitle">
          <img
            class="TitleAvatar"
            shape="square"
            :size="50"
            src="@/assets/logo.png"
          />
          <el-text class="TitleText">自行车自组商城</el-text>
          <el-tag class="TitleTag" type="primary">beta</el-tag>
        </div>
        <el-input
          class="SearchBarInput"
          v-model="input"
          placeholder="请输入搜索内容"
        >
          <template #append>
            <el-button :icon="Search" @click="getSearchResult()" /> </template
        ></el-input>
      </div>
      <!-- 搜索结果 -->
      <el-card class="ResultContainer">
        <template #header>搜索结果</template>
        <el-empty
          description="没有匹配结果！"
          v-if="Object.keys(ResultProfile.data).length === 0"
        />
        <el-row v-else>
          <el-col
            :span="6"
            v-for="(item, index) in ResultProfile.data"
            :key="index"
          >
            <div class="GoodsUnit" @click="toItemDetail(item.item_id)">
              <div class="GoodsImg">
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
          </el-col>
        </el-row>
      </el-card>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, reactive, ref } from 'vue'
import { Search } from '@element-plus/icons-vue'
import { useRoute, useRouter } from 'vue-router'
import baseURL from '@/utils/axios'
import { searchItemApi as searchItem } from '@/apis/item'

const router = useRouter()

const input = ref('')
const ResultProfile = reactive({ data: [] })

// 获取参数
const route = useRoute()
const searchString = route.query.searchString as string
// 唤起搜索
const getSearchResult = () => {
  return searchItem({ searchString: input.value })
    .then((res: any) => {
      ResultProfile.data = res.data.data
    })
    .catch((err: any) => {
      console.log(err)
    })
}
// 加载时唤起搜索
onMounted(async () => {
  try {
    input.value = searchString
    await getSearchResult()
  } catch (error) {
    console.error(error)
  }
})
// 点击能够跳去商品详情
const toItemDetail = (params: any) => {
  const itemId = params.toString()
  router.push({ name: 'item_detail', query: { itemId: itemId } })
}
</script>

<style lang="less" scoped>
@import '@/assets/styles/common.css';
.Search {
  min-height: 100%;
  background-color: #f0f0f0;

  .SearchBar {
    width: 1240px;
    margin: 0 auto;
    position: relative;
    background-color: #f0f0f0;
    padding: 20px 0;
    align-content: center;
    .ShopTitle {
      display: inline-block;
      align-content: center;
      .TitleAvatar {
        width: 75px;
        height: 75px;
      }

      .TitleAvatar,
      .TitleText,
      .TitleTag {
        display: inline-block;
        vertical-align: middle;
        margin: 5px;
      }

      .TitleText {
        font-size: 15px;
        color: black;
        line-height: 50px;
      }
    }
    .SearchBarInput {
      width: 75%;
      height: 40px;
      border-radius: 50px;
      overflow: hidden;
    }
  }

  .ResultContainer {
    background: #ffffff;
    padding: 15px;
    margin-top: 10px;
    border-radius: 15px;

    .GoodsUnit {
      // flex: 1;
      display: inline-block;
      margin: 10px;
      padding: 15px;
      border-radius: 25px;
      box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.218);
      overflow: hidden;

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
  }
}
</style>
