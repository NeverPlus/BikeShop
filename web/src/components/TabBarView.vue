<template>
  <el-header class="TabBar">
    <div class="ShopTitle TabBarContent" @click="toPage('home')">
      <img
        class="TitleAvatar"
        shape="square"
        :size="50"
        src="@/assets/logo.png"
      />
      <el-text class="TitleText">自行车自组商城</el-text>
      <el-tag class="TitleTag" type="primary">beta</el-tag>
    </div>
    <div class="My TabBarFuncArea">
      <el-text>
        你好！ {{ userName }}
      </el-text>
      <el-link
        class="MyText"
        @click="toPage('home')"
        :underline="false"
        target="_self"
        >主页</el-link
      >
      <el-link
        class="MyText"
        @click="toPage('diy')"
        :underline="false"
        target="_self"
        >DIY面板</el-link
      >
      <el-link
        class="MyText"
        @click="toPage('goods')"
        :underline="false"
        target="_self"
        >商品列表</el-link
      >
      <el-link
        class="MyText"
        @click="toPage('my_page')"
        :underline="false"
        target="_self"
        >个人中心</el-link
      >
      <!-- 去购物车还是管理商品 -->
      <el-link
        v-if="userType === 2"
        class="MyText"
        @click="toPage('cart')"
        :underline="false"
        target="_self"
        >购物车</el-link
      >
      <el-link
        v-else-if="userType === 1"
        class="MyText"
        @click="toPage('list_item')"
        :underline="false"
        target="_self"
        >商品列表</el-link
      >
      <!-- 我的订单还是管理订单 -->
      <el-link
        v-if="userType === 2"
        class="MyText"
        @click="toPage('my_orders')"
        :underline="false"
        target="_self"
        >我的订单</el-link
      >
      <el-link
        v-else-if="userType === 1"
        class="MyText"
        @click="toPage('merchant_orders')"
        :underline="false"
        target="_self"
        >管理订单</el-link
      >
    </div>
  </el-header>
</template>

<style lang="less" scoped>
.TabBar {
  display: flex;
  background-color: #cef0a6;
  // border-bottom-right-radius: 20px;
  // border-bottom-left-radius: 20px;
  height: 70px;
  min-width: 1240px;
  padding: 10px;

  .ShopTitle {
    margin-right: auto;
    padding-right: 20px;
    align-content: center;

    .TitleAvatar {
      width: 70px;
      height: 70px;
    }

    .TitleAvatar,
    .TitleText,
    .TitleTag {
      display: inline-block;
      vertical-align: middle;
      margin: 5px;
    }

    .TitleText {
      font-size: 25px;
      color: black;
      line-height: 50px;
    }
  }
  .My {
    .MyText {
      width: 75px;
      margin: 0 10px;
      color: #2c2c2c;
      line-height: 50px;
      transition: all 0.1s linear;
    }

    .MyText:hover {
      background: #a1ab96;
      color: #000000;
      border-radius: 25px;
      transform: scale(1.1);
    }
  }

  .TabBarFuncArea {
    padding-right: 20px;
    margin-left: auto;
  }
}
</style>

<script lang="ts" setup>
import { defineProps } from 'vue'
import { useRouter } from 'vue-router'

// 接收参数
const props = defineProps({
  userType: Number,
  userName: String
})

const router = useRouter()
const toPage = (param: string) => {
  const name = param.toString()
  router.push({ name: name })
}
</script>
<script lang="ts">
export default {
  name: 'TabBar'
}
</script>
