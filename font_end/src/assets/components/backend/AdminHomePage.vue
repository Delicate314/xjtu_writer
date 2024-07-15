<template>
  <div class="content">
    <div class="Info-content">
      <div class="github-corner-wrapper">
        <GitLink />
      </div>
      <div class="Hello">
        <HelloAdmin />
      </div>
      <div class="HomeInfo">
        <HomeInfo />
      </div>
    </div>
    
    <div class="img-container">
      <a href="https://github.com/Delicate314/xjtu_writer" target="_blank">
        <img src="../../assets/backend_logo/gitLogo.jpg" alt="Clickable Image" class="img-git">
      </a>
      <a href="http://121.36.55.149/docs" target="_blank">
        <img src="../../assets/backend_logo/fastapi-logo.png" alt="Clickable Image" class="img-fast">
      </a>
    </div>
  </div>
</template>

<script>
import GitLink from "@/components/backend/gitCorner";
import HelloAdmin from '@/components/backend/HelloAdmin';
import HomeInfo from "@/components/backend/HomeInfo";

export default {
  components: {
    GitLink,
    HelloAdmin,
    HomeInfo
  }
};
</script>

<style scoped>
.content {
  line-height: 2;
}

.Info-content {
  display: flex;
  line-height: 2;
}

.github-corner-wrapper {
  position: absolute;
  top: 70px;
  right: 8px; 
}

.Hello {
  margin-left: 125px;
  margin-top: 150px;
}

.HomeInfo {
  margin-left: 125px;
  margin-top: 100px;
}

.img-container {
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  margin-top: 100px; /* 根据需要调整间距 */
  margin-left: 300px;
}

.img-git{
  margin: 0 15px; /* 调整图片之间的间距 */
  width: 40%; /* 根据需要调整图片大小 */
  height: auto; /* 保持图片的宽高比 */
}
.img-fast{
  margin: 0 15px; /* 调整图片之间的间距 */
  width: 30%; /* 根据需要调整图片大小 */
  height: auto; /* 保持图片的宽高比 */
}
</style>
