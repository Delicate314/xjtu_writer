<template>
    <div class="rank-view">
        <h2 class="title">Rankings</h2>
        <ul>
            <li v-for="(item, index) in rankings" :key="index">
                <span class="rank">{{ item.rank }}</span>
                <span class="novel">{{ item.novel }}</span>
                <span class="author">By {{ item.author }}</span>
                <span class="popularity">热度{{ item.popularity }}</span>
            </li>
        </ul>
    </div>
</template>

<script>
export default {
    data() {
        return {
            rankings: [
                { rank: 1,novel:"novel 1", author: "Author 1", popularity: 99 },
                { rank: 2,novel:"novel 2", author: "Author 2", popularity: 90 },
                { rank: 3,novel:"novel 3",author: "Author 3", popularity: 80 },
                // Add more ranking items here
            ],
        };
    },
};
</script>

<style scoped>
.rank-view {
    margin-top: 20px;
    max-width: 800px;
    margin: 0 auto;
}

.title {
    height: 0px;
    text-align: center;
    margin-bottom: 60px;
    color: white;
    font-family:'Courier New', Courier, monospace;
    font-size: 40px;
}

li{
    display: flex;
    align-items: center;
    justify-content: center;
}

.rank{
    font-family:'微软雅黑';
    font-size: medium;
    padding: 0px 18px;
    color:#eeeeee;
    text-align: left;
    border-bottom: none;
    background-color: #3d84a8;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    resize: none;
    margin: 0px 20px;
}

.novel{
    font-family:'微软雅黑';
    font-size: medium;
    padding: 0px 18px;
    color:#eeeeee;
    text-align: left;
    border-bottom: none;
    background-color: #3d84a8;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    resize: none;
    margin: 0px 20px;

}

.author{
    font-family:'微软雅黑';
    font-size: medium;
    padding: 0px 18px;
    color:#eeeeee;
    background-color: #3d84a8;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    resize: none;
}

.popularity{
    font-family:'微软雅黑';
    font-size: medium;
    padding:0px 18px;
    color:#eeeeee;
    text-align: left;
    border-bottom: none;
    background-color: #3d84a8;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    resize: none;
    margin: 20px;
}
</style>