<template>
    <div class="position">
      <router-link  :key="index" :to="item.path" v-for="(item,index) in $router.options.routes"   >
      <span class="link" v-if="item.meta.isShow">{{ item.meta.name }}</span>
    </router-link>
    </div>
</template>

<script>
export default {
    name: 'Guide_nevel',
};

</script>

<style scoped>
.link {
  font-size: 20px;
  text-decoration: none;
  color: #fff;
  margin: 0 35px;
  padding: 5px 20px;
  border: 3px solid #2271ad;
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
</style>