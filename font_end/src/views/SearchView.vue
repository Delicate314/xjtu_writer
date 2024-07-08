<template>
  <div>
    <router-link :key="index" :to="item.path" v-for="(item, index) in $router.options.routes">
      <span class="link" v-if="item.meta.isShow">{{ item.meta.name }}</span>
    </router-link>
    <h2>搜索小说</h2>
    <input type="text" placeholder="请输入小说名" v-model="query">
    <button @click="search">Search</button>
  </div>
</template>

<script>
export default {
  name: 'SearchView',
  data() {
    return {
      query: '',
    };
  },
  methods: {
    search() {
      console.log('Searching for', this.query);
      // Add your search logic here
    },
  },
};
</script>

<style>
input {
  padding: 10px;
  width: 200px;
  margin-right: 10px;
}

button {
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
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
</style>
