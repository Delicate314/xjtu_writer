<template>
    <div>
        <div class="top">
                <Guide />
        </div>
        <div class="novel-detail">
            <div class="cover-aside">
            <img src="~@/assets/cover.png" alt="A Tale of Two Cities">
            </div>
            <div class="info">
                <h2 class="head">A Tale of Two Cities</h2>
                <h3 class="footer">By Charles John Huffam Dickens</h3>
                <p class="footer">Popularity:114514</p>
                <p class="main">Set against the backdrop of the French Revolution, “A Tale of Two Cities” is a historical novel by Charles Dickens. Published in 1859, the novel tells the story of the intertwining lives of two families - one French and one English - during this tumultuous period. The story is primarily set in London and Paris, hence the title “A Tale of Two Cities.”</p>
                <textarea placeholder="向AI提问" v-model="content" class="footer_ask"></textarea>
                <button @click="save" class='footer_commit'>提交</button>
            </div>
        </div>
    </div>
</template>

<script>
import Guide from '@/components/Guide.vue';

export default {
    name: 'NovelDetail',
    components:{
        Guide,
    },
    data() {
    return {
      content: '',
    };
  },
  methods: {
    save() {
      console.log('提交', this.content);
      // Add your save logic here
    },
  }
};
</script>

<style scoped>
.novel-detail {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 20px;
}

.top{
    display: block;
    align-items: center;
    height: 50px;
}

.cover-aside{
    background-color: #D3DCE6;
    color: #333;
    text-align: center;
    height: 600px;
    width: 500px;
}

.head{
    background-color: #B3C0D1;
    color: #333;
    text-align: center;
    line-height: 50px;
    width: 900px;
    margin: 0%;
    align-items: center;
}

.footer{
    background-color: bisque;
    color: #333;
    text-align: center;
    line-height: 50px;
    width: 900px;
}

.main{
    background-color: chocolate;
    color: #333;
    text-align: center;
    line-height: 50px;
    font-size: medium;
    width: 900px;
}



.info {
    text-align: center;
}

.footer_ask{
    display: block;
    width: 900px;
    padding: 10px;
    margin: 10px auto;
}
.footer_commit {
    padding: 10px 20px;
    background-color: #007bff;
    color: #fff;
    border: none;
    cursor: pointer;
}
</style>