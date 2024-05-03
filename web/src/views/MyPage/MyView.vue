<template>
  <div class="My">
    <div class="Container">
      <el-card class="MyPanel">
        <el-form
          ref="formRef"
          :model="myProfile.newData"
          :rules="rules"
          label-width="auto"
        >
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
          <el-form-item>
            <el-upload
              action="#"
              accept=".jpg, .png"
              :limit="1"
              :auto-upload="true"
              :show-file-list="false"
              :http-request="uploadAvatar"
              ><el-avatar
                v-if="true"
                :size="75"
                :src="baseURL + myProfile.data.avatar"
              />
              <!-- <img  :src="baseURL + myProfile.data.avatar" class="avatar" /> -->
              <el-icon v-else
                ><el-avatar :size="50" src="../assets/logo.png"
              /></el-icon>
            </el-upload>
          </el-form-item>
          <el-form-item label="用户名" prop="username">
            <el-input
              v-model="myProfile.newData.username"
              :input-style="{ textAlign: 'right' }"
              :placeholder="
                !(myProfile.data.username == '')
                  ? myProfile.data.username
                  : '用户名'
              "
              clearable
            ></el-input>
          </el-form-item>
          <el-form-item label="邮箱" prop="email">
            <el-input
              v-model="myProfile.newData.email"
              :input-style="{ textAlign: 'right' }"
              :placeholder="
                !(myProfile.data.email == '')
                  ? myProfile.data.email
                  : '还没有电子邮件！'
              "
              clearable
            ></el-input>
          </el-form-item>
          <el-form-item label="电话号码" prop="phone">
            <el-input
              v-model="myProfile.newData.phone"
              :input-style="{ textAlign: 'right' }"
              :placeholder="
                !(myProfile.data.phone == '')
                  ? myProfile.data.phone
                  : '还没有设置地址！'
              "
              clearable
            ></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="uploadProfile" round>提交</el-button>
          </el-form-item>
          <!-- 其他表单项 -->
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script lang="ts" setup>
import baseURL from '@/utils/axios'
import { getBase64 } from '@/utils/tools'
import {
  userProfileApi as userProfile,
  userAvatarUpdateApi as avatarUpdate,
  userProfileUpdateApi as profileUpdate
} from '@/apis/user'
import { onMounted, reactive, ref } from 'vue'
import { ElMessage, FormInstance, FormRules } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

const formRef = ref<FormInstance>()
const myProfile = reactive({
  data: {},
  newData: {
    isNew: false,
    username: '',
    email: '',
    phone: ''
  }
})

const router = useRouter()

const backPage = () => {
  router.back()
}

const getMyData = async () => {
  return await userProfile({ token: localStorage.getItem('TOKEN') })
    .then((res: any) => {
      console.log(res)
      myProfile.data = res.data.data
    })
    .catch((err) => {
      console.log(err)
      throw err
    })
}

onMounted(async () => {
  try {
    await getMyData()
  } catch (error) {
    console.error(error)
  }
})

// 更新头像
const uploadAvatar = (file: any) => {
  const newAvatar = file.file
  const avatarType = newAvatar.type.replace('image/', '.')
  let avatarString = ''
  // 转码base64
  getBase64(newAvatar)
    .then((res: any) => {
      const params = res.split(',')
      if (params.length > 0) {
        avatarString = params[1]
        // 提交更新
        avatarUpdate({
          token: localStorage.getItem('TOKEN'),
          avatarBase64: avatarString,
          imageType: avatarType
        })
          .then((res: any) => {
            if (res.code === 200) {
              formRef.value.resetFields()
              ElMessage.success('修改头像成功！')
              getMyData()
            }
          })
          .catch((err) => {
            console.log(err)
          })
      }
    })
    .catch((err) => {
      console.log(err)
    })
}

// 校验规则
const validateUsername = (rule: any, value: any, callback: any) => {
  const pattern = /^(?=.*[a-zA-Z])(?=.*[0-9])[^]{4,16}$/

  if (!value) {
    return callback()
  } else if (!pattern.test(value)) {
    callback(new Error('用户名长度在4~16个字符，包含至少一个字母和一个数字'))
  } else {
    callback()
  }
}

const validatePhone = (rule: any, value: any, callback: any) => {
  const pattern = /^1[3|4|5|7|8][0-9]\d{8}$/

  if (!value) {
    return callback()
  } else if (!pattern.test(value)) {
    callback(new Error('请输入正确的电话号码！'))
  } else {
    callback()
  }
}

// 设定校验
const rules = reactive<FormRules<typeof myProfile.newData>>({
  username: [{ validator: validateUsername, trigger: 'blur' }],
  phone: [{ validator: validatePhone, trigger: 'blur' }],
  email: [
    {
      message: '请输入电子邮箱',
      trigger: 'blur'
    },
    {
      type: 'email',
      message: '请输入正确的邮箱地址',
      trigger: ['blur', 'change']
    }
  ]
})

const uploadProfile = () => {
  if (!formRef.value) return
  formRef.value.validate((valid) => {
    if (valid) {
      profileUpdate({
        token: localStorage.getItem('TOKEN'),
        username: myProfile.newData.username,
        email: myProfile.newData.email,
        phone: myProfile.newData.phone
      })
        .then((res: any) => {
          if (res.code === 200) {
            formRef.value.resetFields()
            ElMessage.success('修改信息成功！')
            getMyData()
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
.My {
  min-height: 100%;
  margin: 0;
  background-color: #f0f0f0;

  .Container {
    padding: 15px;
    .MyPanel {
      border-radius: 25px;
      padding: 20px;
      .backButton {
        float: left;
      }
    }
  }
}
</style>
