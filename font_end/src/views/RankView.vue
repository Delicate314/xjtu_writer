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
  };
  </script>
  