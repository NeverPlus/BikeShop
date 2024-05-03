<template>
  <!-- 注册页面 -->
  <!-- 注册背景 -->
  <div class="Register">
    <!-- 注册面板 -->
    <div class="RegisterPanel">
      <!-- 注册表格 -->
      <el-container>
        <el-header class="PanelName">用户注册</el-header>
        <el-main class="PanelContent">
          <el-form
            ref="formRef"
            :model="form"
            :rules="rules"
            label-width="auto"
            style="max-width: 600px"
          >
            <el-form-item label="用户名" prop="username">
              <el-input
                v-model="form.username"
                placeholder="用户名长度在4~16个字符，包含至少一个字母和一个数字"
              />
            </el-form-item>
            <el-form-item label="密码" prop="password">
              <el-input
                v-model="form.password"
                type="password"
                :show-password="true"
                placeholder="密码长度在8个字符以上，包含至少一个字母和一个数字"
              />
            </el-form-item>
            <el-form-item label="再次输入密码" prop="checkPass">
              <el-input
                v-model="form.checkPass"
                type="password"
                :show-password="true"
              />
            </el-form-item>
            <el-form-item label="电话" prop="phone">
              <el-input v-model="form.phone" />
            </el-form-item>
            <el-form-item label="邮件" prop="email">
              <el-input
                v-model="form.email"
                placeholder="example@example.com"
              />
            </el-form-item>
            <el-form-item label="地址" prop="address">
              <el-input v-model="form.address" />
            </el-form-item>
            <el-form-item label="用户类型" prop="character">
              <el-radio-group v-model="form.character">
                <el-radio value="2">用户</el-radio>
                <el-radio value="1">商家</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item class="Link">
              <el-link @click="toLogin" :underline="false" target="_self"
                >已有用户？前去登录。</el-link
              >
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="submitForm()">注册</el-button>
              <el-button @click="resetForm(formRef)">清空</el-button>
            </el-form-item>
          </el-form>
        </el-main>
      </el-container>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { FormInstance, FormRules } from 'element-plus'
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { registerApi as register } from '@/apis/register'

const router = useRouter()

const toLogin = () => {
  router.push({ name: 'login' })
}

const formRef = ref<FormInstance>()

const form = reactive({
  username: '',
  password: '',
  checkPass: '',
  email: '',
  phone: '',
  address: '',
  character: '2'
})

// 校验规则
const validateUsername = (rule: any, value: any, callback: any) => {
  const pattern = /^(?=.*[a-zA-Z])(?=.*[0-9])[^]{4,16}$/

  if (!value) {
    return callback(new Error('请输入用户名'))
  }
  setTimeout(() => {
    if (!pattern.test(value)) {
      callback(new Error('用户名长度在4~16个字符，包含至少一个字母和一个数字'))
    } else {
      callback()
    }
  }, 500)
}

const validatePassword = (rule: any, value: any, callback: any) => {
  const pattern = /^(?=.*[a-zA-Z])(?=.*[0-9])[^]{8,}$/

  if (!value) {
    return callback(new Error('请输入密码'))
  } else if (!pattern.test(value)) {
    callback(new Error('密码长度在8个字符以上，包含至少一个字母和一个数字'))
  } else {
    if (form.checkPass !== '') {
      if (!formRef.value) return
      formRef.value.validateField('checkPass', () => null)
    }
    callback()
  }
}

const validatePhone = (rule: any, value: any, callback: any) => {
  const pattern = /^1[3|4|5|7|8][0-9]\d{8}$/

  if (!value) {
    return callback(new Error('请输入电话'))
  } else if (!pattern.test(value)) {
    callback(new Error('请输入正确的电话号码！'))
  } else {
    callback()
  }
}

const validateCheck = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('请再次输入密码!'))
  } else if (value !== form.password) {
    callback(new Error('两次输入不一致！'))
  } else {
    callback()
  }
}

// 设定校验
const rules = reactive<FormRules<typeof form>>({
  username: [{ validator: validateUsername, trigger: 'blur', required: true }],
  password: [{ validator: validatePassword, trigger: 'blur', required: true }],
  checkPass: [{ validator: validateCheck, trigger: 'blur', required: true }],
  phone: [{ validator: validatePhone, trigger: 'blur', required: true }],
  email: [
    {
      required: false,
      message: '请输入电子邮箱',
      trigger: 'blur'
    },
    {
      type: 'email',
      message: '请输入正确的邮箱地址',
      trigger: ['blur', 'change']
    }
  ],
  character: [
    {
      required: true,
      message: '请选择用户类型',
      trigger: 'change'
    }
  ]
})

const submitForm = () => {
  if (!formRef.value) return
  formRef.value.validate((valid) => {
    if (valid) {
      register(form)
        .then((res: any) => {
          if (res.code === 200) {
            localStorage.setItem('TOKEN', res.data.token)
            console.log(res)
          }
        })
        .catch((err: any) => {
          console.log(err)
        })
      // console.log('submit!')
      router.push({ name: 'login' })
    } else {
      console.log('error submit!')
      return false
    }
  })
}

const resetForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.resetFields()
}
</script>

<style lang="less" scoped>
@import '@/assets/styles/common.css';
.Register {
  min-height: 100%;
  margin: 0;
  padding: 1px;
  background-color: rgb(216, 255, 255);

  .RegisterPanel {
    margin: auto;
    margin-top: 150px;
    width: 600px;

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
        margin-left: auto;
      }

      .el-button {
        border-radius: 25px;
        margin: auto;
        width: 75px;
        height: 30px;
      }
    }
  }
}
</style>
