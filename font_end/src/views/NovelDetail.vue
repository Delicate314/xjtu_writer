<template>
    <div class="novel-detail">
        <div class="cover-aside">
           <img src="~@/assets/cover.png" alt="A Tale of Two Cities">
        </div>
        <div class="info">
            <h2 class="head">A Tale of Two Cities</h2>
            <h3 class="footer">By Charles John Huffam Dickens</h3>
            <p class="footer">Popularity:114514</p>
            <p class="main">Set against the backdrop of the French Revolution, “A Tale of Two Cities” is a historical novel by Charles Dickens. Published in 1859, the novel tells the story of the intertwining lives of two families - one French and one English - during this tumultuous period. The story is primarily set in London and Paris, hence the title “A Tale of Two Cities.”</p>
        </div>
    </div>
</template>

<script>

export default {
    name: 'NovelDetail',
};
</script>

<style scoped>
.novel-detail {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 20px;
}

.cover-aside{
    background-color: #D3DCE6;
    color: #333;
    text-align: center;
    line-height: 100px;
    width: 1500px;
}

.head{
    background-color: #B3C0D1;
    color: #333;
    text-align: center;
    line-height: 100px;
}

.footer{
    background-color: bisque;
    color: #333;
    text-align: center;
    line-height: 50px;
}

.main{
    background-color: chocolate;
    color: #333;
    text-align: center;
    line-height: 100px;
    font-size: medium;
}



.info {
    text-align: center;
}
</style>