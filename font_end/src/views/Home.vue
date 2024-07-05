<template>
  <div class="home-container">
    <StarryBackground />
    <h1 class="gradient-text">欢迎来到XJTU小说家！</h1>
    <router-link to="/search" class="link">搜索小说</router-link> |
    <router-link to="/write" class="link">小说续写</router-link> |
    <router-link to="/login" class="link">用户登录</router-link> |
    <router-link to="/register" class="link">用户注册</router-link>
  </div>
</template>

<script>
import StarryBackground from '../components/StarryBackground.vue';

export default {
  name: 'Home',
  components: {
    StarryBackground,
  },
};
</script>

<style>
.home-container {
  position: relative;
  z-index: 1;
}

h1 {
  margin-top: 20px;
  font-size: 2em;
  background: linear-gradient(90deg, white 25%, transparent 25%) repeat-x;
  background-size: 200% 100%;
  animation: gradient 10s linear infinite;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

@keyframes gradient {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

.link {
  text-decoration: none;
  color: #007bff;
  margin: 0 10px;
  padding: 5px 10px;
  border: 2px solid #007bff;
  border-radius: 15px;
  display: inline-block;
  transition: all 0.3s ease;
  position: relative;
}

.link:hover {
  color: #fff;
  background-color: #007bff;
  animation: jelly 0.5s;
}

@keyframes jelly {
  0%, 100% {
    transform: scale(1, 1);
  }
  25% {
    transform: scale(0.9, 1.1);
  }
  50% {
    transform: scale(1.1, 0.9);
  }
  75% {
    transform: scale(0.95, 1.05);
  }
}
</style>
