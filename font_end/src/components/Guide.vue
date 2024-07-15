<template>
  <div class="position">
    <h1 class="gradient-text">Welcome to XJTU AI-Writer! :)</h1>
    <router-link :key="index" :to="item.path" v-for="(item, index) in $router.options.routes">
      <span class="link" v-if="item.meta.isShow">{{ item.meta.name }}</span>
    </router-link>
  </div>
</template>

<script>
export default {
  name: 'Guide',
};

</script>

<style scoped>
.link {
  font-size: 20px;
  font-weight: bold;
  text-decoration: none;
  color: #fff;
  box-shadow: 0 4px 8px rgba(6, 0, 125, 0.1);
  margin: 0 35px;
  padding: 5px 20px;
  border-radius: 15px;
  border: 3px solid #eeeeee;
  display: inline-block;
  transition: all 0.3s ease;
  position: relative;
}

.link:hover {
  color: #fff;
  background-color: #007bff;
  animation: jelly 0.5s;
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
  font-weight: bold;
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