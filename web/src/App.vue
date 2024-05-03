<template>
  <TabBar
    :user-type="myProfile.data.user_type"
    :userName="myProfile.data.username"
  />
  <router-view />
  <footer>
    <FooterView />
  </footer>
</template>

<style lang="less">
html,
body,
#app {
  margin: 0;
  padding: 0;
  height: 100%;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;

  min-width: 1240px;
}

nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>

<script lang="ts" setup>
import TabBar from '@/components/TabBarView.vue'
import FooterView from '@/components/FooterView.vue'
import { userProfileApi as userProfile } from '@/apis/user'
import { onMounted, reactive } from 'vue'

const myProfile = reactive({
  data: {}
})
// 启动加载
onMounted(async () => {
  const token = localStorage.getItem('TOKEN')
  if (token !== null && token.length > 0) {
    try {
      await getMyData()
    } catch (error) {
      console.error(error)
    }
  }
})
// 加载用户数据
const getMyData = async () => {
  return await userProfile({ token: localStorage.getItem('TOKEN') })
    .then((res: any) => {
      // console.log(res)
      myProfile.data = res.data.data
    })
    .catch((err) => {
      console.log(err)
      throw err
    })
}
// 判断用户类型
// 传递参数给tabbar
</script>

<script lang="ts">
export default {}
</script>
