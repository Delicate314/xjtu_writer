<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
import StarryBackground from './components/StarryBackground.vue';

export default {
  name: 'App',
  components: {
    StarryBackground,
  },
};
</script>

<style>
/* 添加你的全局样式 */


#app {
  text-align: center;
  position: relative;
  overflow: hidden;
}
</style>
