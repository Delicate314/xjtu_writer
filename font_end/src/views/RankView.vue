<template>
  <div>
    <StarryBackground />
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

export default {
  name: 'RankView',
  components: {
    StarryBackground,
    Guide,
    RankTable,
    RankOfWriter,
  },
};
</script>