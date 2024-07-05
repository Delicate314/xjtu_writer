<template>
  <div class="starry-background">
    <div class="stars layer1"></div>
    <div class="stars layer2"></div>
    <div class="stars layer3"></div>
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

.stars {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: transparent url('/public/stars.png') repeat;
  animation: moveStars 100s linear infinite;
  opacity: 0.5;
}

.layer2 {
  background: transparent url('/public/stars2.png') repeat;
  animation: moveStars 200s linear infinite;
  opacity: 0.5;
}

.layer3 {
  background: transparent url('/public/stars3.png') repeat;
  animation: moveStars 300s linear infinite;
  opacity: 0.5;
}

@keyframes moveStars {
  from { transform: translateY(0); }
  to { transform: translateY(-1000px); }
}
</style>
