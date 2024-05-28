<template>
  <div class="ListItem">
    <div class="Container">
      <el-card class="ListItemPanel">
        <template #header
          ><el-button class="backButton" type="default" round @click="backPage"
            ><el-icon class="MyNavUnitIcon"><ArrowLeft /></el-icon
            >返回</el-button
          ><span class="CardHeader">已上架商品</span></template
        >
        <el-empty
          description="暂时没有商品！"
          v-if="Object.keys(itemsProfile.data).length === 0"
        />
        <div class="ListItemContent" v-else>
          <div
            class="ListItemUnit"
            v-for="item in itemsProfile.data"
            :key="item.item_id"
          >
            <div class="itemImg">
              <img :src="baseURL + item.item_image" alt="" height="100%" />
            </div>
            <div class="itemProfile">
              <el-descriptions :title="item.item_name">
                <el-descriptions-item label="商品种类">{{
                  item.item_type
                }}</el-descriptions-item>
                <el-descriptions-item label="剩余数量">{{
                  item.item_quantity
                }}</el-descriptions-item>
                <el-descriptions-item label="当前定价">{{
                  item.price
                }}</el-descriptions-item>
              </el-descriptions>
            </div>
            <div class="itemAction">
              <el-button round type="primary" @click="toEdit(item.item_id)"
                >修改</el-button
              >
              <el-button
                round
                type="danger"
                @click="confirmDelete(item.item_id)"
                >删除</el-button
              >
            </div>
          </div>
        </div>
        <template #footer>
          <el-button round type="default" @click="toPage('add_item')">
            添加商品
          </el-button>
        </template>
      </el-card>
    </div>

    <!-- 确认删除 -->
    <el-dialog
      class="dialog"
      v-model="deleteItemDialog"
      title="Tips"
      width="500"
    >
      <span>确认删除？</span>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="cancelDelete" round>取消</el-button>
          <el-button type="danger" @click="handleDelete" round>
            删除
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import baseURL from '@/utils/axios'
import {
  getMerchantItemApi as getMerchantItem,
  deleteItemApi as deleteItem
} from '@/apis/item'
import { onMounted, reactive, ref } from 'vue'
import { FormInstance } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

const formRef = ref<FormInstance>()
const itemsProfile = reactive({ data: [] })

const router = useRouter()

const backPage = () => {
  router.back()
}
const toEdit = (params: any) => {
  const itemId = params.toString()
  router.push({ name: 'edit_item', query: { itemId: itemId } })
}
const toPage = (param: string) => {
  const name = param.toString()
  router.push({ name: name })
}

const getMerchantItemData = async () => {
  return await getMerchantItem({ token: localStorage.getItem('TOKEN') })
    .then((res: any) => {
      itemsProfile.data = res.data.data
      console.log(itemsProfile.data)
    })
    .catch((err) => {
      console.log(err)
      throw err
    })
}

onMounted(async () => {
  try {
    await getMerchantItemData()
  } catch (error) {
    console.error(error)
  }
})

// 删除商品
const deleteItemDialog = ref(false)
const itemToDelete = ref()
const confirmDelete = (itemId: any) => {
  itemToDelete.value = itemId
  deleteItemDialog.value = true
}

const cancelDelete = () => {
  itemToDelete.value = null
  deleteItemDialog.value = false
}

const handleDelete = () => {
  deleteItemDialog.value = false
  return deleteItem({ itemId: itemToDelete.value })
    .then((res) => {
      getMerchantItemData()
      console.log(res)
    })
    .catch((err) => {
      console.log(err)
    })
}

// 进入编辑界面
</script>
<script lang="ts">
export default {}
</script>

<style lang="less" scoped>
@import '@/assets/styles/common.css';
.ListItem {
  min-height: 100%;
  margin: 0;
  background-color: #f0f0f0;

  .Container {
    padding: 15px;
    .ListItemPanel {
      border-radius: 25px;
      padding: 20px;
      .backButton {
        float: left;
      }
      .ListItemContent {
        .ListItemUnit {
          display: flex;
          margin-bottom: 10px;
          padding: 10px;
          border: 1px solid #e7e7e7;
          border-radius: 25px;
          .itemImg {
            display: inline-block;
            width: 125px;
            height: 125px;
            border: 1px solid #e7e7e7;
            border-radius: 15px;
            overflow: hidden;
          }
          .itemProfile {
            display: inline-block;
            min-width: 600px;
            padding-left: 20px;
          }
          .itemAction {
            margin-left: auto;
          }
        }
      }
    }
  }
}
</style>
