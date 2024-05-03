<template>
  <div class="Diy">
    <div class="Container">
      <el-card class="DiyPanel">
        <el-tabs v-model="activePanel" class="Diytabs">
          <el-tab-pane label="公路车" name="Road Bike">
            <DiyTab bike-type="Road" />
          </el-tab-pane>
          <el-tab-pane label="山地车" name="Hill Bike">
            <DiyTab bike-type="Hill" />
          </el-tab-pane>
        </el-tabs>
      </el-card>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, reactive, ref } from 'vue'
import DiyTab from './components/DiyTab.vue'

// 选择组装哪种自行车
const activePanel = ref('Road Bike')

</script>
<script lang="ts">
export default {}
</script>

<style lang="less" scoped>
@import '@/assets/styles/common.css';
.Diy {
  margin: 0;
  background-color: #f0f0f0;

  .Container {
    padding: 15px;
    .DiyPanel {
      border-radius: 25px;
    }
  }
}
.ItemsPanel {
  border-radius: 25px;

  .ItemUnit {
    // flex: 1;
    display: inline-block;
    margin: 10px;
    padding: 15px;
    border-radius: 25px;
    box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.218);
    overflow: hidden;

    .ItemImg {
      height: 150px;
      width: 150px;
      border: 1px solid #e7e7e7;
      border-radius: 25px;
      overflow: hidden;
    }

    .ItemDesc {
      .ItemName {
        display: block;
        padding: 5px 5px;
        font-size: 25px;
        text-align: left;
      }
      .ItemNum {
        display: block;
        padding: 2px 5px;
        font-size: 15px;
        text-align: left;
      }
      .ItemSale {
        display: flex;
        padding: 5px;
        .ItemPrice {
          display: inline-block;
          flex: 4;
          text-align: left;
        }
        .ItemBuy {
          display: inline-block;
          flex: 1;
        }
      }
    }
  }
}
</style>
