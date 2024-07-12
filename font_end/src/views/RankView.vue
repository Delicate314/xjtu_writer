<template>
    <div>
            <div class="rank-view">
                <Background />
                <Guide />
                <h2 class="title">小说排名</h2>
                <table>
                    <thead>
                        <tr>
                            <th class="rank-top">排名</th>
                            <th>书名</th>
                            <th>作者</th>
                            <th>热度</th>
                            <th class="rank-bottom">简介</th>
                        </tr>
                    </thead>
                    <tbody class="rank-item">
                            <td>index=1</td>
                        <router-link :to="'/Novel'" class="item-link">
                            <td>novel-1-title</td>
                        </router-link>
                        <td>novel-1-author</td>
                        <td>novel-1-popularity</td>
                        <td>novel-1-description</td>
                    </tbody>
                    <tbody class="rank-item">
                        <td>index=2</td>
                        <router-link :to="'/Novel'" class="item-link">
                        <td>novel-2-title</td>
                        </router-link>
                        <td>novel-2-author</td>
                        <td>novel-2-popularity</td>
                        <td>novel-2-description</td>
                    </tbody>
                </table>
            </div>
        <div>
        <!--
            <ul>
            <li v-for="(item, index) in novels" :key="index">
                <span class="rank">{{ index + 1 }}</span>
                <span class="author">{{ item.author }}</span>
                <span class="popularity">{{ item.popularity }}</span>
            </li>
            </ul>
        -->
        </div>
    </div>
</template>

<script>
import Guide from '@/components/Guide.vue';
import Background from '@/components/Background.vue';

export default {
    name: 'RankView',
    components: {
        Guide,
        Background,
    },
    data(){
        return {
            novels: [],
        };
    },
};
</script>

<style scoped>
.rank-view {
    max-width: 1000px;
    margin-top: 20px;
    margin: 0 auto;
    margin-top: 20px;
}

.title {
    height: 0px;
    text-align: center;
    margin-bottom: 100px;
    color: white;
    font-family:'Courier New', Courier, monospace;
    font-size: 40px;
}
.item-link{
    text-decoration: none;
    color: #eeeeee;
}

table {
    width: 100%;
    border-collapse: collapse;
}


th{
    font-family:'微软雅黑';
    font-size: 20px;
    padding: 10px 16px;
    text-align: center;
    background-color: #00adb5;
}

.rank-top{
    border-top-left-radius: 10px;
    border-bottom-left-radius: 10px;
}

.rank-bottom{
    border-top-right-radius: 10px;
    border-bottom-right-radius: 10px;
}

td {
    font-family:'微软雅黑';
    font-size: medium;
    padding: 18px;
    color:#eeeeee;
    text-align: left;
    border-bottom: none;
    background-color: #393e46;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    resize: none;
    margin: 20px;
}

/*.rank{
    padding: 10px 18px;
    color:#eeeeee;
    text-align: left;
    border-bottom: 1px solid #110202;
    background-color: #393e46;
}

.author{
    padding: 18px;
    color:#eeeeee;
    text-align: left;
    border-bottom: 1px solid #110202;
    background-color: #393e46;
}

.popularity{
    padding: 18px;
    color:#eeeeee;
    text-align: left;
    border-bottom: 1px solid #110202;
    background-color: #393e46;
}
*/
</style>
</style>