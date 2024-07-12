<template>
  <div class="home-container">
    <StarryBackground />
    <Guide />
    <Home_rank />
  </div>
</template>

<script>
import StarryBackground from '../components/StarryBackground.vue';
import Element from '../components/Element.vue';
import Guide from '../components/Guide.vue';
import Home_rank from '@/components/Home_rank.vue';

export default {
  name: 'Home',
  components: {
    StarryBackground,
    Element,
    Guide,
    Home_rank,
  },
};
</script>

<style>
.home-container {
  position: relative;
  z-index: 1;
}
</style>
