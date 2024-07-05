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
body {
  font-family: Arial, sans-serif;
  background-color: #f0f0f0;
  margin: 0;
  padding: 0;
}
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  position: relative;
  overflow:hidden;
}
</style>
