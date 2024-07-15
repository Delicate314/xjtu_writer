<template>
  <div class="home-container">
    <StarryBackground />
    <Guide />
    <RankTable />
    <UserInfo />
    <!-- <UserNovel /> -->
  </div>
</template>

<script>
import StarryBackground from '../components/StarryBackground.vue';
import Element from '../components/Element.vue';
import Guide from '../components/Guide.vue';
import RankTable from '@/components/RankTable.vue';
import UserInfo from '@/components/UserInfo.vue';
import UserNovel from '@/components/UserNovel.vue';

export default {
  name: 'Home',
  components: {
    StarryBackground,
    Element,
    Guide,
    RankTable,
    UserInfo,
    //UserNovel,
  },
};
</script>

<style>
.home-container {
  position: relative;
  z-index: 1;
  display: block;
  justify-content: center;
  /* 让内部元素水平居中 */
}
</style>
