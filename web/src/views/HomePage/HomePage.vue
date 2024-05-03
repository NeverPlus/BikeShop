<template>
  <div class="HomePage">
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
            <el-button :icon="Search" @click="toSearch('search')" /> </template
        ></el-input>
      </div>
      <div class="ContentContainer">
        <!-- 轮播图 -->
        <GoodsCarousel />
        <!-- 商品种类 -->
        <TypeCard />
        <!-- 商品卡片 -->
        <GoodsCard title="零件推荐" type="Parts" />
        <!-- 商品卡片 -->
        <GoodsCard title="整车推荐" type="Bikes" />
      </div>
    </div>
  </div>
</template>

<style lang="less" scoped>
@import '@/assets/styles/common.css';
.HomePage {
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

  .ContentContainer {
    background: #ffffff;
    padding: 15px;
    margin-top: 10px;
    border-radius: 15px;
  }

  .PartsHot,
  .BikeHot {
    img {
      display: inline-block;
    }
  }
}
</style>

<script lang="ts" setup>
import GoodsCarousel from './components/GoodsCarousel.vue'
import GoodsCard from './components/GoodsCard.vue'
import TypeCard from './components/TypeCard.vue'

import { ref } from 'vue'
import { Search } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

const input = ref('')

const router = useRouter()
const toPage = (param: string) => {
  const name = param.toString()
  router.push({ name: name })
}

const toSearch = (param: string) => {
  if (input.value.length > 0) {
    const name = param.toString()
    router.push({ name: name, query: { searchString: input.value } })
  }
}
</script>
