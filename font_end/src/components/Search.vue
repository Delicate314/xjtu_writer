<template>
  <div class="search-container">
    <h2>Search for Novels</h2>
    <input type="text" placeholder="Enter novel name" v-model="query">
    <button @click="search">Search</button>
  </div>
</template>

<script>
export default {
  name: 'Search',
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
.search-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
  background-color: #fff;
}
input {
  display: block;
  width: 100%;
  padding: 10px;
  margin: 10px 0;
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
