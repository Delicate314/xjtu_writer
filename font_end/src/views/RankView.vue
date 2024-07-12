<template>
    <div class="rank_background">
        <h1 class="gradient-text">Welcome to XJTU-AI Writer! :)</h1>
        <router-link :key="index" :to="item.path" v-for="(item, index) in $router.options.routes">
            <span class="link" v-if="item.meta.isShow">{{ item.meta.name }}</span>
        </router-link>
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
import { RouterLink } from 'vue-router';

export default {
    name: 'RankView',
};
</script>

<style scoped>
.rank_background {
    background-image: url('@/assets/rank_background.jpg');
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
    height: 100vh;
    width: 100%;
    opacity: 1.0;
    position: relative;
    margin: 0px;
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

.link {
  text-decoration: none;
  background-color: #ffffff;
  color: #007bff;
  margin: 10px 10px;
  padding: 5px 15px;
  border: 2px solid #aa9393;
  border-radius: 15px;
  display: inline-block;
  transition: all 0.3s ease;
  position: relative;
  opacity: 0.7;
  font-size: 20px;
  font-family: "微软雅黑";
  font-weight: bold;
  /* 或者使用其他数值来调整粗细程度 */
}

.link:hover {
  color: #fff;
  background-color: #007bff;
  animation: jelly 0.5s;
}
</style>