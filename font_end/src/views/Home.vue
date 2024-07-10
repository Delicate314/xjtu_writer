<template>
  <div class="home-container">
    <StarryBackground />
    <h1 class="gradient-text">Welcome to XJTU AI-Writer! :)</h1>
    <router-link :key="index" :to="item.path" v-for="(item, index) in $router.options.routes" >
      <span class="link" v-if="item.meta.isShow">{{ item.meta.name }}</span>
    </router-link>
    <div class="rank-view">
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
          <tr>
            <td>1</td>
            <td>
              <div class="novel-info-box">
                <router-link :to="'/Novel'">novel-1-title</router-link>
              </div>
            </td>
            <td>novel-1-author</td>
            <td>novel-1-popularity</td>
            <td>novel-1-description</td>
          </tr>
          <tr>
            <td>2</td>
            <td>
              <div class="novel-info-box">
                novel-2-title
              </div>
            </td>
            <td>novel-2-author</td>
            <td>novel-2-popularity</td>
            <td>novel-2-description</td>
          </tr>
          <tr>
            <td>3</td>
            <td>
              <div class="novel-info-box">
                novel-3-title
              </div>
            </td>
            <td>novel-3-author</td>
            <td>novel-3-popularity</td>
            <td>novel-3-description</td>
          </tr>
        </tbody>
      </table>
    </div>
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

<style scoped>
.home-container {
  position: relative;
  z-index: 1;
}


@keyframes gradient {
  0% {
    background-position: 150% 0;
  }
  100% {
    background-position: -150% 0;
  }
}

h1 {
  font-size: 2em;
  background: linear-gradient(90deg, #ffffff 25%, #0309c2 50%, #5a315d 75%);
  background-size: 150% 100%;
  animation: gradient 15s ease infinite;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
  font-family: Verdana, Geneva, Tahoma, sans-serif;
  margin: 0px;
  padding: 10px 10px;
  font-weight: bold;
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

.novel-info-box {
  padding: 10px;
  border: 2px solid #aaa;
  border-radius: 10px;
  background-color: #fff;
  text-align: center;
}
</style>
