<template>
  <div class="home-container">
    <Background />
    <Guide />
    <UserInfo />
    <!-- <UserNovel /> -->
  </div>
</template>

<script>
import StarryBackground from '../components/StarryBackground.vue';
import Guide from '../components/Guide.vue';
import Background from '@/components/Background.vue';
import UserInfo from '@/components/UserInfo.vue';
import UserNovel from '@/components/UserNovel.vue';

export default {
  name: 'Home',
  components: {
    Guide,
    UserInfo,
    Background
    //UserNovel,
  },
};
</script>

<style>
.home-container {
  position: relative;
  z-index: 1;
  display: block;
  justify-content: center;
  /* 让内部元素水平居中 */
}
</style>
