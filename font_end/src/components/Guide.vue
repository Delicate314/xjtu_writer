<template>
    <div>
      <router-link to="/search" class="link">搜索小说</router-link> |
      <router-link to="/write" class="link">小说续写</router-link> |
      <router-link to="/Home" class="link">推荐</router-link> |
      <router-link to="/Rank" class="link">小说排行</router-link>
    </div>
</template>

<script>
export default {
    name: 'Guide',
};

</script>

<style>


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