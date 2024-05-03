<template>
  <div class="AddItem">
    <div class="Container">
      <el-card class="AddItemPanel">
        <template #header>
          <el-button class="backButton" type="default" round @click="backPage"
            ><el-icon class="MyNavUnitIcon"><ArrowLeft /></el-icon
            >返回</el-button
          >
          <span class="CardHeader">添加商品</span></template
        >
        <el-form ref="formRef" :model="form" style="max-width: 750px">
          <!-- 商品图片 -->
          <el-form-item label="商品图">
            <el-upload
              ref="itemImage"
              action="#"
              list-type="picture-card"
              :http-request="addItemRequest"
              :limit="1"
              :on-exceed="handleExceed"
              :auto-upload="false"
            >
              <el-icon><Plus /></el-icon>

              <template #file="{ file }">
                <div>
                  <img
                    class="el-upload-list__item-thumbnail"
                    :src="file.url"
                    alt=""
                  />
                  <span class="el-upload-list__item-actions">
                    <span
                      v-if="!disabled"
                      class="el-upload-list__item-delete"
                      @click="handleRemove(file)"
                    >
                      <el-icon><Delete /></el-icon>
                    </span>
                  </span>
                </div>
              </template>
              <template #tip>
                <div class="el-upload__tip text-red">
                  仅限单张图，新图片会覆盖
                </div>
              </template>
            </el-upload>
          </el-form-item>
          <!-- 商品名字 -->
          <el-form-item label="商品名" prop="name">
            <el-input
              v-model="form.name"
              placeholder="请输入商品名字"
            ></el-input>
          </el-form-item>
          <!-- 商品类型 -->
          <el-form-item label="商品类型" prop="type">
            <el-select v-model="form.type" placeholder="商品类型">
              <el-option
                v-for="item in itemType"
                :key="item.id"
                :label="item.item_type"
                :value="item.id"
              />
            </el-select>
            <!-- 商品数量 -->
          </el-form-item>
          <el-form-item label="商品数量" prop="quantity">
            <el-input-number v-model="form.quantity" :min="0" />
          </el-form-item>
          <!-- 商品价格 -->
          <el-form-item label="商品价格" prop="price">
            <el-input-number
              v-model="form.price"
              :precision="2"
              :step="0.1"
              :min="0.0"
              controls-position="right"
            />
          </el-form-item>
          <!-- 商品详细描述 -->
          <el-form-item label="商品描述图片">
            <el-upload
              ref="itemDescImage"
              action="#"
              list-type="picture-card"
              :http-request="handleItemDesc"
              :limit="3"
              :auto-upload="false"
              :file-list="itemDescImgFiles.data"
              :on-change="handleChange"
              :multiple="true"
            >
              <el-icon><Plus /></el-icon>

              <template #file="{ file }">
                <div>
                  <img
                    class="el-upload-list__item-thumbnail"
                    :src="file.url"
                    alt=""
                  />
                  <span class="el-upload-list__item-actions">
                    <span
                      v-if="!descDisabled"
                      class="el-upload-list__item-delete"
                      @click="handleDescRemove(file)"
                    >
                      <el-icon><Delete /></el-icon>
                    </span>
                  </span>
                </div>
              </template>
              <template #tip>
                <div class="el-upload__tip text-red">最多3张图片</div>
              </template>
            </el-upload>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitForm()" round
              >添加</el-button
            >
            <el-button @click="resetForm(formRef)" round>清空</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, reactive, ref } from 'vue'
import {
  FormInstance,
  UploadFile,
  UploadInstance,
  UploadProps,
  UploadRawFile,
  genFileId
} from 'element-plus'
import { Delete, Plus, ArrowLeft } from '@element-plus/icons-vue'
import {
  addItemApi as addItem,
  allItemTypeApi as ItemType,
  addItemDescApi as addItemDesc
} from '@/apis/item'
import { getBase64, getBase64List } from '@/utils/tools'
import { useRouter } from 'vue-router'

const itemType = ref([])
const router = useRouter()

const backPage = () => {
  router.back()
}

const getItemType = () => {
  return ItemType({})
    .then((res: any) => {
      const result = res.data.data
      result.forEach((element: any) => {
        itemType.value.push(element)
      })
      return result
    })
    .catch((err) => {
      console.error(err)
      throw err
    })
}

onMounted(async () => {
  try {
    await getItemType()
  } catch (error) {
    console.error(error)
  }
})

const formRef = ref<FormInstance>()
const form = reactive({
  name: '',
  type: '',
  quantity: 0,
  price: 0.0
})

// 处理请求
const addItemRequest = (file: any) => {
  const itemImage = file.file
  const imageType = itemImage.type.replace('image/', '.')
  let imageString = ''
  let uploadItem = {}
  // 转码base64
  getBase64(itemImage)
    .then((res: any) => {
      const params = res.split(',')
      if (params.length > 0) {
        imageString = params[1]

        // 验证表单并合并数据
        if (!formRef.value) return
        formRef.value
          .validate((valid) => {
            if (valid) {
              uploadItem = {
                token: localStorage.getItem('TOKEN'),
                imageBase64: imageString,
                imageType: imageType,
                ...form
              }
            }
          })
          .then((res) => {
            // 提交更新
            addItem(uploadItem)
              .then((res) => {
                // 商品介绍图上传
                getBase64List(itemDescImgFiles.data).then((res: any) => {
                  const regex = /^data:image\/(\w+);base64,/
                  const imageDescStrings = [] as any
                  res.forEach((element: any) => {
                    const type = element.match(regex)[1]
                    const params = element.split(',')
                    let imgString = ''
                    if (params.length > 0) {
                      imgString = params[1]
                    }
                    imageDescStrings.push({
                      imageBase64: imgString,
                      imageType: type
                    })
                  })
                  // 导入接口
                  addItemDesc({
                    token: localStorage.getItem('TOKEN'),
                    name: form.name,
                    imgString: imageDescStrings
                  }).then((res) => {
                    console.log(res)
                  })
                  router.push({ name: 'list_item' })
                })
              })
              .catch((err) => {
                console.log(err)
              })
          })
          .then()
          .catch((err) => {
            console.log(err)
          })
      }
    })
    .catch((err) => {
      console.log(err)
    })
}

const submitForm = () => {
  itemImage.value!.submit()
}

const resetForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.resetFields()
}

// 上传图片缩略图
const itemImage = ref<UploadInstance>()
const disabled = ref(false)

const handleRemove = (file: UploadFile) => {
  itemImage.value.handleRemove(file)
}

const handleExceed: UploadProps['onExceed'] = (files) => {
  itemImage.value!.clearFiles()
  const file = files[0] as UploadRawFile
  file.uid = genFileId()
  itemImage.value!.handleStart(file)
}

// 上传商品描述图
const itemDescImage = ref<UploadInstance>()
const itemDescImgFiles = reactive({ data: [] })
const descDisabled = ref(false)

const handleChange = (file: any, files: any) => {
  itemDescImgFiles.data = files
  console.log(itemDescImgFiles.data)
}

const handleItemDesc = (file: any) => {
  console.log('')
}

const handleDescRemove = (file: UploadFile) => {
  itemDescImage.value.handleRemove(file)
}
</script>

<script lang="ts">
export default {}
</script>

<style lang="less" scoped>
@import '@/assets/styles/common.css';
.AddItem {
  min-height: 100%;
  margin: 0;
  background-color: #f0f0f0;

  .Container {
    padding: 15px;
    .AddItemPanel {
      border-radius: 25px;
      padding: 20px;
      .backButton {
        float: left;
      }

      el-form > el-form-item {
        margin: auto;
      }
    }
  }
}
</style>
