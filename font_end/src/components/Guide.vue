<template>
    <div class="head">
        <router-link to="/search" class="link">搜索小说</router-link> 
        <router-link to="/write" class="link">AI创作</router-link> 
        <router-link to="/login" class="link">用户登录</router-link> 
        <router-link to="/register" class="link">用户注册</router-link> 
        <router-link to="/rank" class="link">小说排名</router-link>
    </div>
</template>

<script>
export default {
    name: 'Guide',
};

</script>

<style>

.head{
    background-color: #B3C0D1;
    color: #333;
    text-align: center;
    line-height: 100px;
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
</style>