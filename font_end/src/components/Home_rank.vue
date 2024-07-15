<template>
    <div class="rank-view">
        <h2 class="title">Ranking</h2>
        <ul>
            <li v-for="(item, index) in filteredRankings" :key="index">
                <span class="rank">{{ index+1 }}</span>
                <span class="novel">{{ item.novel_title }}</span>
                <span class="author">By {{ item.user_name }}</span>
                <span class="popularity">热度{{ item.novel_viewcount }}</span>
            </li>
        </ul>
    </div>
</template>

<script>
export default {
    name: 'RankView',
    data() {
        return {
            rankings: [],
        };
    },
    computed: {
        filteredRankings() {
        // 过滤 rankings 数组，只返回索引 0 到 2 的元素
        return this.rankings.filter((_, index) => index >= 0 && index < 3);
        }
    },
    mounted() {
        this.get_homeRank();
    },
    method:{
        async get_homeRank() {
            console.log('Fetching novel rank...');
            try {
                const params={
                    index:1,
                };
                const response = await this.$axios.get('https://121.36.55.149:80/apis/rank',params);
                this.rankings = response.data;
                console.log('Rank:', rankings);
            } catch (error) {
                console.error('Error fetching novel rank:', error);
            }
        }
    }
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