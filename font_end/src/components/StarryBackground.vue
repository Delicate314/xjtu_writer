<template>
  <div class="starry-background">
    <video autoplay muted loop id="background-video">
      <source src="/stars.mp4" type="video/mp4" />
      您的浏览器不支持视频标签。
    </video>
  </div>
</template>

<script>
export default {
  name: 'StarryBackground',
};
</script>

<style>
.starry-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: -1;
}

#background-video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>
