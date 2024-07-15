<template>
  <div>
    <StarryBackground />
    <Guide />
    <RankTable />
  </div>
</template>

<script>
import StarryBackground from '@/components/StarryBackground.vue';
import Guide from '@/components/Guide.vue';
import RankTable from '@/components/RankTable.vue';

export default {
  name: 'RankView',
  components: {
    StarryBackground,
    Guide,
    RankTable,
  },
  mounted() {
    this.checkOrientation();
    window.addEventListener('resize', this.checkOrientation);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.checkOrientation);
  },
  methods: {
    checkOrientation() {
      if (window.innerHeight > window.innerWidth) {
        alert('请横屏获得最佳体验(´︶｀)');
      }
    }
  }
};
</script>