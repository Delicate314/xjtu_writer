<template>
  <div>
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
</style>
