<template>
  <div class="MyPage">
    <div class="Container">
      <el-card class="MyPagePanel">
        <div class="MyProfile">
          <el-avatar
            class="MyAvatar"
            :src="baseURL + myProfile.data.avatar"
          ></el-avatar>
          <el-text class="MyName">{{ myProfile.data.username }}</el-text>
        </div>
        <!-- <el-card class="MyOrder">
          <template #header>我的订单</template>
          <div class="MyOrderStatus">
            <el-text class="StatusText">待付款</el-text>
          </div>
          <div class="MyOrderStatus">
            <el-text class="StatusText">待发货</el-text>
          </div>
          <div class="MyOrderStatus">
            <el-text class="StatusText">运送中</el-text>
          </div>
          <div class="MyOrderStatus">
            <el-text class="StatusText">待签收</el-text>
          </div>
          <div class="MyOrderStatus">
            <el-text class="StatusText">已完成</el-text>
          </div>
        </el-card> -->
        <div class="MyNav">
          <div class="MyNavUnit" @click="toPage('my')">
            <el-text class="MyNavUnitText">修改个人资料</el-text
            ><el-icon class="MyNavUnitIcon"><ArrowRight /></el-icon>
          </div>
          <div
            class="MyNavUnit"
            @click="
              myProfile.data.user_type == 2
                ? toPage('my_orders')
                : toPage('merchant_orders')
            "
          >
            <el-text class="MyNavUnitText">订单管理</el-text
            ><el-icon class="MyNavUnitIcon"><ArrowRight /></el-icon>
          </div>
          <div
            v-if="myProfile.data.user_type == 2"
            class="MyNavUnit"
            @click="toPage('my_address')"
          >
            <el-text class="MyNavUnitText">地址管理</el-text
            ><el-icon class="MyNavUnitIcon"><ArrowRight /></el-icon>
          </div>
          <div v-else class="MyNavUnit" @click="toPage('list_item')">
            <el-text class="MyNavUnitText">商品管理</el-text
            ><el-icon class="MyNavUnitIcon"><ArrowRight /></el-icon>
          </div>
          <div class="MyNavUnit" @click="toPage('my_settings')">
            <el-text class="MyNavUnitText">账号与安全</el-text
            ><el-icon class="MyNavUnitIcon"><ArrowRight /></el-icon>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ArrowRight } from '@element-plus/icons-vue'
import { onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import baseURL from '@/utils/axios'
import { userProfileApi as userProfile } from '@/apis/user'

const myProfile = reactive({
  data: {}
})

const router = useRouter()
const toPage = (param: string) => {
  const name = param.toString()
  router.push({ name: name })
}

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

onMounted(async () => {
  const token = localStorage.getItem('TOKEN')
  if (token === null || token.length <= 0) {
    toPage('login')
  } else {
    try {
      await getMyData()
    } catch (error) {
      console.error(error)
    }
  }
})
</script>
<script lang="ts">
export default {}
</script>

<style lang="less" scoped>
@import '@/assets/styles/common.css';
.MyPage {
  min-height: 100%;
  margin: 0;
  background-color: #f0f0f0;

  .Container {
    padding: 15px;

    .MyPagePanel {
      border-radius: 25px;
      .MyProfile {
        display: flex;
        padding: 10px;
        .MyName {
          padding-left: 15px;
          font-size: large;
          font-weight: 600;
        }
      }
      .MyOrder {
        background: #eaeaea;
        border-radius: 25px;
        border: 1px solid #cbcbcb;
        margin-bottom: 10px;
        .MyOrderStatus {
          width: 20%;
          display: inline-block;
          .StatusText {
            line-height: 50px;
            padding: 25px 50px;
            border-radius: 25px;
            border: 1px solid #cbcbcb;
          }
        }
      }
      .MyNav {
        .MyNavUnit {
          display: flex;
          padding: 20px;
          border-bottom: 1px solid #f0f0f0;
          border-radius: 25px;
          transition: all 0.1s linear;

          .MyNavUnitIcon {
            margin-left: auto;
          }
        }
        .MyNavUnit:hover {
          background: #bbedff;
          transform: scale(1.01);
        }
      }
    }
  }
}
</style>
