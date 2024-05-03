<template>
  <div class="MyAddress">
    <div class="Container">
      <el-card class="MyAddressPanel">
        <el-form
          ref="formRef"
          :model="myProfile.newData"
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
          <el-form-item label="地址" prop="address">
            <el-input
              v-model="myProfile.newData.address"
              :input-style="{ textAlign: 'right' }"
              :placeholder="
                !(myProfile.data.address == '')
                  ? myProfile.data.address
                  : '还没有地址！'
              "
              clearable
            ></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="uploadProfile" round
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
    address: ''
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

const uploadProfile = () => {
  if (!formRef.value) return
  formRef.value.validate((valid) => {
    if (valid) {
      profileUpdate({
        token: localStorage.getItem('TOKEN'),
        address: myProfile.newData.address
      })
        .then((res: any) => {
          if (res.code === 200) {
            formRef.value.resetFields()
            ElMessage.success('修改地址成功！')
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
.MyAddress {
  min-height: 100%;
  margin: 0;
  background-color: #f0f0f0;

  .Container {
    padding: 15px;
    .MyAddressPanel {
      border-radius: 25px;
      padding: 20px;
      .backButton {
        float: left;
      }
    }
  }
}
</style>
