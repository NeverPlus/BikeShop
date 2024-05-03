<template>
  <footer class="Footer">
    <div class="FooterContent">
      一个基于Django+Vue的自行车自组商城<br />
      Copyright ©2024 -计算机203陈鼎熹. All Rights Resvered
    </div>
  </footer>
</template>

<script lang="ts" setup></script>
<script lang="ts">
export default {
  name: 'FooterView'
}
</script>

<style lang="less" scoped>
.Footer {
  display: flex;
  justify-content: center;
  align-content: center;
  background-color: #353535;
  .FooterContent {
    height: 100px;
    text-align: center;
    line-height: 40px;
    color: #e4e4e4;
  }
}
</style>
