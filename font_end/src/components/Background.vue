<template>
    <div class="background">
        <img :src="`/${this.$route.meta.background}`" alt="" class="background-img"/>
    </div>
  </template>
  
  <script>
  export default {
    name: 'Background',
  };
  </script>
  
  <style scoped>
  .background {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    z-index: -1;
  }
  
  .background-img {
    position: absolute;
    top: 0;
    left: 0; 
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  </style>
  