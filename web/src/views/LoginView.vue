<template>
  <!-- 登录页面 -->
  <!-- 登录背景 -->
  <div class="Login">
    <!-- 登录面板 -->
    <div class="LoginPanel">
      <el-container>
        <el-header class="PanelName">欢迎来到自行车自组商城！</el-header>
        <el-main class="PanelContent">
          <el-form
            ref="formRef"
            :model="form"
            label-width="auto"
            style="max-width: 300px"
          >
            <el-form-item label="用户名">
              <el-input v-model="form.username" /> </el-form-item
            ><el-form-item label="密码">
              <el-input
                type="password"
                :show-password="true"
                v-model="form.password"
              />
            </el-form-item>
            <el-form-item>
              <el-link
                @click="toRegister('forget_password')"
                :underline="false"
                target="_self"
                >忘记密码？</el-link
              >
              |
              <el-link
                @click="toRegister('home')"
                :underline="false"
                target="_self"
                >先逛一逛？</el-link
              >
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="onSubmit">登录</el-button>
              <el-button @click="toRegister('register')">注册</el-button>
            </el-form-item>
          </el-form>
        </el-main>
      </el-container>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ElMessage, FormInstance, FormRules } from 'element-plus'
import { onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { loginApi as login } from '@/apis/login'

const router = useRouter()
const toRegister = (param: string) => {
  const name = param.toString()
  router.push({ name: name })
}

onMounted(() => {
  if (localStorage.getItem('TOKEN')) {
    router.push({ name: 'my_page' })
  }
})

// do not use same name with ref
const formRef = ref<FormInstance>()

const form = reactive({
  username: '',
  password: ''
})

const onSubmit = () => {
  if (!formRef.value) return
  formRef.value.validate((valid: any) => {
    if (valid) {
      login(form)
        .then((res: any) => {
          if (res.code === 200) {
            localStorage.setItem('TOKEN', res.data.token)
            router.push({ name: 'home' })
          }
          // console.log(res)
        })
        .catch((err: any) => {
          console.log(err)
        })
    } else {
      ElMessage.warning('请填写登录信息!')
    }
  })
  // console.log('submit!')
}
</script>

<style lang="less" scoped>
@import '@/assets/styles/common.css';
.Login {
  min-height: 100%;
  margin: 0;
  background-image: url('@/assets/images/Background.jpg');
  background-repeat: no-repeat;
  background-size: cover;

  // background-color: rgb(216, 255, 255);

  .LoginPanel {
    float: right;
    margin-top: 150px;
    margin-right: 20%;
    width: 350px;

    background: #ffffff;
    border-radius: 25px;
    box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.218);

    .PanelName {
      margin: auto;
      padding: 20px 10px;
      color: rgb(0, 0, 0);
      font-size: 20px;
      text-align: center;
      font-weight: bold;
      line-height: 30px;
      letter-spacing: 2px;
    }

    .PanelContent {
      .el-link {
        margin: auto;
        float: right;
      }

      .el-button {
        border-radius: 25px;
        margin: auto;
      }
    }
  }
}
</style>
