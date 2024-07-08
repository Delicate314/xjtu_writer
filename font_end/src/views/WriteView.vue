<template>
  <div>
    <router-link to="/search" class="link">搜索小说</router-link> |
    <router-link to="/write" class="link">小说续写</router-link> |
    <router-link to="/Home" class="link">推荐</router-link>|
    <router-link to="/Rank" class="link">小说排行</router-link>
    <h2>XJTU小说续写家</h2>
    <textarea placeholder="续写你的小说~" v-model="content"></textarea>
    <button @click="save" class='save'>提交</button>
    <button @click="save" class='genshin'>元神</button>
    <button @click="save" class='genshit'>明朝</button>
    <button @click="save" class='genshil'>巴萨</button>
    <button @click="save" class='shit'>詹姆斯</button>
  </div>
</template>

<script>

export default {
  name: 'WriteView',
  data() {
    return {
      content: '',
    };
  },
  methods: {
    save() {
      console.log('提交', this.content);
      // Add your save logic here
    },
  },
};
</script>

<style>
textarea {
  width: 300px;
  height: 150px;
  padding: 10px;
  margin-top: 10px;
  margin-bottom:1000px;
}
button {
  padding: 10px 20px;
  background-color: #00ff88;
  color: #fff;
  border: none;
  cursor: pointer;
}
button:hover {
  background-color: #00b35f;
}
.link {
  text-decoration: none;
  top:0;
  left:0;
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

.save{
  color:white;
  position:absolute;
  top:300px;
  left:727px;
}
.genshil{
  color:white;
  position:absolute;
  top:350px;
  left:590px;
  box-sizing: content-box;
  border-radius:30px
}
.genshin{
  color:white;
  position:absolute;
  top:350px;
  left:680px;
  box-sizing: content-box;
  border-radius:30px
}
.shit{
  color:white;
  position:absolute;
  top:350px;
  left:770px;
  box-sizing: content-box;
  border-radius:30px
}
.genshit{
  color:white;
  position:absolute;
  top:350px;
  left:500px;
  box-sizing: content-box;
  border-radius:30px
}
</style>
