<template>
  <div class="home-container">
    <StarryBackground />
    <h1 class="gradient-text">欢迎来到XJTU-AI Writer!</h1>
    <router-link  :key="index" :to="item.path" v-for="(item,index) in $router.options.routes"   >
      <span class="link" v-if="item.meta.isShow">{{ item.meta.name }}</span>
    </router-link>
    <!-- <router-link to="/Home" class="link">主页</router-link> |
    <router-link to="/search" class="link">搜索小说</router-link> |
    <router-link to="/write" class="link">小说续写</router-link> |
    <router-link to="/Rank" class="link">小说排行</router-link> -->
    <h2 class="title">小说排名</h2>
    <table>
      <thead>
        <tr>
          <th>排名</th>
          <th>书名</th>
          <th>作者</th>
          <th>热度</th>
          <th>简介</th>
        </tr>
      </thead>
      <tbody>
        <td>index=1</td>
        <router-link :to="'/Novel'">
          <td>novel-1-title</td>
        </router-link>
        <td>novel-1-author</td>
        <td>novel-1-popularity</td>
        <td>novel-1-description</td>
      </tbody>
      <tbody>
        <td>index=2</td>
        <td>novel-2-title</td>
        <td>novel-2-author</td>
        <td>novel-2-popularity</td>
        <td>novel-2-description</td>
      </tbody>
      <tbody>
        <td>index=3</td>
        <td>novel-3-title</td>
        <td>novel-3-author</td>
        <td>novel-3-popularity</td>
        <td>novel-3-description</td>
      </tbody>
    </table>
  </div>
</template>

<script>
import StarryBackground from '../components/StarryBackground.vue';
import Element from '../components/Element.vue';


export default {
  name: 'Home',
  components: {
    StarryBackground,
    Element
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
  top: 0;
  left: 0;
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

  0%,
  100% {
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

.rank-view {
  max-width: 800px;
  margin: 0 auto;
}

.title {
  height: 0px;
  text-align: center;
  margin-bottom: 60px;
  color: aqua;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 8px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #f2f2f2;
}
</style>
