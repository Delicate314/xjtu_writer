<template>
  <div>
    <Background />

    <Guide />
    <RankTable />
    <RankOfWriter />
  </div>
</template>

<script>
import StarryBackground from '@/components/StarryBackground.vue';
import Guide from '@/components/Guide.vue';
import RankTable from '@/components/RankTable.vue';
import RankOfWriter from '../components/RankOfWriter.vue';
import Background from '@/components/Background.vue';

export default {
  name: 'RankView',
  components: {
    StarryBackground,
    Guide,
    RankTable,
    RankOfWriter,
    Background,
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