<template>
  <div class="GoodsCarousel">
    <el-carousel trigger="click">
      <el-carousel-item
        class="carouselItem"
        v-for="(item, index) in announcement.data"
        :key="index"
      >
        <div class="carouselItemBox">
          <el-text class="title">{{ item.title }}</el-text>
          <el-text class="content">{{ item.content }}</el-text>
          <el-text class="date">公告时间：{{ item.post_date }}</el-text>
        </div>
      </el-carousel-item>
    </el-carousel>
  </div>
</template>

<style lang="less" scoped>
.GoodsCarousel {
  height: 300px;
  margin: auto;
  margin-bottom: 10px;
  border-radius: 15px;
  overflow: hidden;
  .carouselItem {
    background: #ffffff;
    .carouselItemBox {
      padding: 10px 80px;
      height: 100%;
      transition: all 0.2s linear;
      .title {
        display: block;
        text-align: left;
        color: #58a3ff;
        font-size: 40px;
        line-height: 60px;
      }
      .content {
        display: block;
        text-align: left;
        font-size: 50px;
        line-height: 150px;
      }
      .date {
        display: block;
        text-align: left;
        font-size: 15px;
        line-height: 50px;
      }
    }
    .carouselItemBox:hover {
      background: #d0d0d0;
    }
  }
}
</style>

<script lang="ts" setup>
import { onMounted, reactive, toRefs } from 'vue'
import { getAnnouncementsApi as getAnnouncements } from '@/apis/announcement'
const state = reactive({
  url: 'https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png'
})
const { url } = toRefs(state)

// 获取轮播图数据
const announcement = reactive({ data: [] })
const getAnnouncementProfile = () => {
  return getAnnouncements({})
    .then((res: any) => {
      if (res.code === 200) {
        announcement.data = res.data.data
        console.log(announcement.data)
      }
    })
    .catch((err) => {
      console.error(err)
      throw err
    })
}

onMounted(async () => {
  try {
    await getAnnouncementProfile()
  } catch (error) {
    console.error(error)
  }
})
</script>
<script lang="ts">
export default {
  name: 'GoodsCarousel'
}
</script>
