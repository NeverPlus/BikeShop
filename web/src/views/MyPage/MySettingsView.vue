<template>
  <div class="MySettings">
    <div class="Container">
      <el-card class="MySettingsPanel">
        <template #header
          ><el-button class="backButton" type="default" round @click="backPage"
            ><el-icon class="MyNavUnitIcon"><ArrowLeft /></el-icon
            >返回</el-button
          >
          <span class="CardHeader">账户与安全</span></template
        >
        <div class="MyNavUnit" @click="toPage('change_password')">
          <el-text class="MyNavUnitText">修改密码</el-text>
        </div>
        <div class="MyNavUnit" @click="logOut()">
          <el-text class="MyNavUnitText">退出登录</el-text>
        </div>
        <div class="MyNavUnit" @click="unRegisterDialog = true">
          <el-text class="MyNavUnitText" style="color: brown">注销用户</el-text>
        </div>
      </el-card>
    </div>
  </div>

  <!-- 确认注销用户 -->
  <el-dialog class="dialog" v-model="unRegisterDialog" title="Tips" width="500">
    <span>确认注销？<br />注销用户无法撤回！</span>
    <template #footer>
      <div class="dialog-footer">
        <el-button type="primary" @click="unRegisterDialog = false" round
          >取消</el-button
        >
        <el-button type="danger" @click="unRegister" round>注销</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script lang="ts" setup>
import { ArrowLeft } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { ref } from 'vue'

const router = useRouter()

const backPage = () => {
  router.back()
}

const toPage = (param: string) => {
  const name = param.toString()
  router.push({ name: name })
}

const logOut = () => {
  localStorage.removeItem('TOKEN')
  router.push({ name: 'login' })
}

const unRegister = () => {
  // 发起请求
  // 删除token
  // localStorage.removeItem('TOKEN')
  // router.push({ name: 'login' })
}

const unRegisterDialog = ref(false)
</script>
<script lang="ts">
export default {}
</script>

<style lang="less" scoped>
@import '@/assets/styles/common.css';
.MySettings {
  min-height: 100%;
  margin: 0;
  background-color: #f0f0f0;

  .Container {
    padding: 15px;

    .MySettingsPanel {
      border-radius: 25px;

      .backButton {
        float: left;
      }

      .MyProfile {
        display: flex;
        padding: 10px;
        .MyName {
          padding-left: 15px;
          font-size: large;
          font-weight: 600;
        }
      }
      .MyNavUnit {
        margin-bottom: 10px;
        padding: 20px;
        border-radius: 25px;
        border: 1px solid #f0f0f0;
        transition: all 0.1s linear;
      }

      .MyNavUnit:hover {
        background: #d7d7d7;
        transform: scale(1.01);
      }
    }
  }
}
</style>
