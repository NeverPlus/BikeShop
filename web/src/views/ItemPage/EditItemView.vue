<template>
  <div class="EditItem">
    <div class="Container">
      <el-card class="EditItemPanel">
        <template #header
          ><el-button class="backButton" type="default" round @click="backPage"
            ><el-icon class="MyNavUnitIcon"><ArrowLeft /></el-icon
            >返回</el-button
          >
          <span class="CardHeader">修改商品</span></template
        >
        <el-form ref="formRef" :model="form" style="max-width: 750px">
          <!-- 商品图片 -->
          <el-form-item label="商品图">
            <!-- 待处理 -->
            <el-upload
              ref="itemImage"
              action="#"
              list-type="picture-card"
              :http-request="editItemRequest"
              :limit="1"
              :on-change="handleChange"
              :on-exceed="handleExceed"
              :auto-upload="false"
            >
              <img
                v-if="!newImage"
                class="el-upload-list__item-thumbnail"
                :src="baseURL + itemProfile.data.item_image"
                alt=""
              />
              <el-icon v-else><Plus /></el-icon>

              <template #file="{ file }">
                <div>
                  <img
                    class="el-upload-list__item-thumbnail"
                    :src="file.url"
                    alt=""
                  />
                  <span class="el-upload-list__item-actions">
                    <span
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
              :placeholder="
                '请输入商品新名字，原名字:' + itemProfile.data.item_name
              "
            ></el-input>
          </el-form-item>
          <!-- 商品类型 -->
          <el-form-item label="商品类型" prop="type">
            <el-select
              v-model="form.type"
              :placeholder="
                '修改商品类型，原类型:' + itemProfile.data.item_type
              "
            >
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
          <!-- 商品描述图 -->
          <el-form-item label="商品描述图">
            <div
              class="itemDescImgs"
              v-for="(image, index) in itemProfile.data.item_desc"
              :key="index"
            >
              <img :src="baseURL + image" width="100%" alt="" />
            </div>
          </el-form-item>
          <el-form-item label="上传新描述图">
            <el-upload
              ref="itemDescImage"
              action="#"
              list-type="picture-card"
              :http-request="handleItemDesc"
              :limit="3"
              :on-change="handleDescChange"
              :auto-upload="false"
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
                      class="el-upload-list__item-delete"
                      @click="handleDescRemove(file)"
                    >
                      <el-icon><Delete /></el-icon>
                    </span>
                  </span>
                </div>
              </template>
              <template #tip>
                <div class="el-upload__tip text-red">仅限3张图</div>
              </template>
            </el-upload>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitForm()" round
              >提交修改</el-button
            >
            <el-button @click="resetForm(formRef)" round>还原</el-button>
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
import {
  Delete,
  Download,
  Plus,
  ZoomIn,
  ArrowLeft
} from '@element-plus/icons-vue'
import baseURL from '@/utils/axios'
import {
  getItemApi as getItem,
  allItemTypeApi as ItemType,
  editItemApi as editItem,
  editItemDescApi as editItemDesc
} from '@/apis/item'
import { getBase64, getBase64List } from '@/utils/tools'
import { useRoute, useRouter } from 'vue-router'
const router = useRouter()
const route = useRoute()
const itemId = route.query.itemId
const itemType = ref([])
const itemProfile = reactive({ data: {} })

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

const getItemProfile = () => {
  return getItem({ itemId: itemId })
    .then((res: any) => {
      console.log(res.data.data)
      itemProfile.data = res.data.data
      form.quantity = parseInt(itemProfile.data.item_quantity)
      form.price = parseFloat(itemProfile.data.price)
      form.type = itemProfile.data.item_type
    })
    .catch((err) => {
      console.error(err)
      throw err
    })
}

onMounted(async () => {
  try {
    await getItemType()
    await getItemProfile()
  } catch (error) {
    console.error(error)
  }
})

const formRef = ref<FormInstance>()
const form = reactive({
  image: false,
  name: '',
  type: '',
  quantity: 0,
  price: 0.0
})

// 处理请求
const editItemRequest = (file: any) => {
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
        form.image = true

        // 验证表单并合并数据
        if (!formRef.value) return
        formRef.value
          .validate((valid) => {
            if (valid) {
              uploadItem = {
                token: localStorage.getItem('TOKEN'),
                itemId: itemId,
                imageBase64: imageString,
                imageType: imageType,
                ...form
              }
            }
          })
          .then((res) => {
            // 提交更新
            editItem(uploadItem).then((res) => {
              // 先转码
              getBase64List(itemDescImgFiles.data)
                .then((res: any) => {
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
                  console.log(imageDescStrings)

                  // 唤起新描述图请求
                  editItemDesc({
                    token: localStorage.getItem('TOKEN'),
                    itemId: itemId,
                    imgString: imageDescStrings
                  }).then((res) => {
                    console.log(res)
                  })
                })
                .catch((err) => {
                  console.log(err)
                })
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
  // 判断有没有修改图片
  if (newImage.value) {
    itemImage.value!.submit()
    router.push({ name: 'list_item' })
  } else {
    let uploadItem = {}
    if (!formRef.value) return
    formRef.value
      .validate((valid) => {
        if (valid) {
          uploadItem = {
            itemId: itemId,
            ...form
          }
        }
      })
      .then((res) => {
        // 提交更新
        editItem(uploadItem)
          .then((res) => {
            getBase64List(itemDescImgFiles.data)
              .then((res: any) => {
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
                console.log(imageDescStrings)

                // 唤起新描述图请求
                editItemDesc({
                  token: localStorage.getItem('TOKEN'),
                  itemId: itemId,
                  imgString: imageDescStrings
                }).then((res) => {
                  console.log(res)
                })
              })
              .catch((err) => {
                console.log(err)
              })
            // router.push({ name: 'list_item' })
            // console.log(res)
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
}

const resetForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.resetFields()
  form.quantity = parseInt(itemProfile.data.item_quantity)
  form.price = parseFloat(itemProfile.data.price)
}

// 上传图片缩略图
const itemImage = ref<UploadInstance>()
const disabled = ref(false)
const newImage = ref(false)

const handleRemove = (file: UploadFile) => {
  itemImage.value.handleRemove(file)
  newImage.value = false
}

const handleChange = (file: UploadFile) => {
  newImage.value = !newImage.value
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

const handleItemDesc = (file: any) => {
  console.log('')
}

const handleDescRemove = (file: UploadFile) => {
  itemDescImage.value.handleRemove(file)
}

const handleDescChange = (file: any, files: any) => {
  itemDescImgFiles.data = files
  console.log(itemDescImgFiles.data)
}
</script>

<script lang="ts">
export default {
  name: 'EditItem'
}
</script>

<style lang="less" scoped>
@import '@/assets/styles/common.css';
.EditItem {
  min-height: 100%;
  margin: 0;
  background-color: #f0f0f0;

  .Container {
    padding: 15px;
    .EditItemPanel {
      border-radius: 25px;
      padding: 20px;
      .backButton {
        float: left;
      }

      el-form > el-form-item {
        margin: auto;
      }
      .itemDescImgs {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 150px;
        height: 150px;
        margin: 10px;
        overflow: hidden;
        border-radius: 25px;
        border: 1px dashed #c2c2c2;
      }
    }
  }
}
</style>
