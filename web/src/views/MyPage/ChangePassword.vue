<template>
  <div class="ChangePassword">
    <div class="Container">
      <el-card class="ChangePasswordPanel">
        <el-form
          ref="formRef"
          :model="passwordForm"
          :rules="rules"
          label-width="auto"
        >
          <!-- 返回键 -->
          <el-form-item
            ><el-button
              class="backButton"
              type="default"
              round
              @click="backPage"
              ><el-icon class="MyNavUnitIcon"><ArrowLeft /></el-icon
              >返回</el-button
            ></el-form-item
          >
          <el-form-item label="旧密码" prop="password" required>
            <el-input
              v-model="passwordForm.password"
              type="password"
              :show-password="true"
              placeholder="请输入旧密码"
            />
          </el-form-item>
          <el-form-item label="新密码" prop="newPassword">
            <el-input
              v-model="passwordForm.newPassword"
              type="newPassword"
              :show-password="true"
              placeholder="密码长度在8个字符以上，包含至少一个字母和一个数字"
            />
          </el-form-item>
          <el-form-item label="再次输入新密码" prop="checkNewPass">
            <el-input
              v-model="passwordForm.checkNewPass"
              type="password"
              :show-password="true"
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="passwordUpdate" round
              >提交</el-button
            >
          </el-form-item>
          <!-- 其他表单项 -->
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { userPasswordUpdateApi as userPasswordUpdate } from '@/apis/user'
import { reactive, ref } from 'vue'
import { ElMessage, FormInstance, FormRules } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

const formRef = ref<FormInstance>()
const passwordForm = reactive({
  password: '',
  newPassword: '',
  checkNewPass: ''
})

const router = useRouter()

const backPage = () => {
  router.back()
}

// 校验规则
const validatePassword = (rule: any, value: any, callback: any) => {
  const pattern = /^(?=.*[a-zA-Z])(?=.*[0-9])[^]{8,}$/

  if (!value) {
    return callback(new Error('请输入密码'))
  } else if (!pattern.test(value)) {
    callback(new Error('密码长度在8个字符以上，包含至少一个字母和一个数字'))
  } else {
    if (passwordForm.newPassword !== '') {
      if (!formRef.value) return
      formRef.value.validateField('checkNewPass', () => null)
    }
    callback()
  }
}

const validateCheck = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('请再次输入新密码!'))
  } else if (value !== passwordForm.newPassword) {
    callback(new Error('两次输入不一致！'))
  } else {
    callback()
  }
}

// 设定校验
const rules = reactive<FormRules<typeof passwordForm>>({
  newPassword: [
    { validator: validatePassword, trigger: 'blur', required: true }
  ],
  checkNewPass: [{ validator: validateCheck, trigger: 'blur', required: true }]
})

const passwordUpdate = () => {
  if (!formRef.value) return
  formRef.value.validate((valid) => {
    if (valid) {
      userPasswordUpdate({
        token: localStorage.getItem('TOKEN'),
        oldPassword: passwordForm.password,
        newPassword: passwordForm.newPassword
      })
        .then((res: any) => {
          if (res.code === 200) {
            formRef.value.resetFields()
            ElMessage.success('修改信息成功！')
            console.log(res.data)
          }
        })
        .catch((err: any) => {
          console.log(err)
        })
    } else {
      console.log('error submit!')
      return false
    }
  })
}
</script>
<script lang="ts">
export default {}
</script>

<style lang="less" scoped>
@import '@/assets/styles/common.css';
.ChangePassword {
  min-height: 100%;
  margin: 0;
  background-color: #f0f0f0;

  .Container {
    padding: 15px;
    .ChangePasswordPanel {
      border-radius: 25px;
      padding: 20px;
      .backButton {
        float: left;
      }
    }
  }
}
</style>
