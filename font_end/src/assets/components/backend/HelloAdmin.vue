<template>
  <div class="admin-container">
    <img src="@/assets/backend_logo/user.gif" alt="Admin Image" class="admin-image">
    <div class="admin-text">
      <div class="hello-text">
        <p>XJTU小说家</p>
        <p>后台管理系统</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HelloAdmin'
};
</script>

<style scoped>
.admin-container {
  line-height: 1;
  display: flex;
  align-items: center; 
}

.admin-image {
  width: 200px; /* 根据需要调整图片大小 */
  height: 200px; /* 根据需要调整图片大小 */
  border-radius: 50%; /* 圆形图片 */
  margin-right: 40px; /* 图片和文字间的间距 */
}

.admin-text {
  display: flex;
  flex-direction: column;
  justify-content: center; /* 垂直居中对齐 */
  font-size: 30px; /* 放大字体 */
  line-height: 2; /* 调整行间距 */
  font-weight: bold; /* 设置文字加粗 */
}

.hello-text {
  font-size: 40px; /* 放大 "Hello !" 的字体 */
  margin: 0; /* 去除默认的外边距 */
  font-weight: bold; /* 设置文字加粗 */
  line-height: 1;
}
</style>
