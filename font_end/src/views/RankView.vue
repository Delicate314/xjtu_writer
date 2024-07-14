<template>
    <div>
            <div class="top">
                <Background />
                <Guide />
                <h2 class="title">小说排名</h2>
                <table>
                    <thead>
                        <tr>
                            <th class="rank-top">排名</th>
                            <th>书名</th>
                            <th>作者</th>
                            <th class="rank-bottom">热度</th>
                        </tr>
                    <!--
                    </thead>
                    <tbody class="rank-item">
                            <td>index=1</td>
                        <router-link :to="'/Novel'" class="item-link">
                            <td>novel-1-title</td>
                        </router-link>
                        <td>novel-1-author</td>
                        <td>novel-1-popularity</td>
                    </tbody> -->
                    </thead>
                    <!-- <tbody class="rank-item">
                            <td>index=1</td>
                        <router-link :to="'/Novel'" class="item-link">
                            <td>novel-1-title</td>
                        </router-link>
                        <td>novel-1-author</td>
                        <td>novel-1-popularity</td>
                    </tbody> -->
                        <tbody v-for="(item, index) in novels" :key="index" class="rank-item">
                            <td>{{ index+1  }}</td>
                            <router-link :to="`/Novel?id=${item.novel_id}`" class="item-link">
                                <td>{{ item.novel_title }}</td>
                            </router-link>
                            <td>{{ item.user_name}}</td>
                            <td>{{ item.novel_viewcount }}</td>
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
    mounted() {
        this.getRank();
    },
    methods: {
        async getRank() {
            console.log('Fetching novel rank...');
            try {
                const params={
                    index:1,
                };
                // console.log('Params:', params);
                const response = await this.$axios.post('http://121.36.55.149:80/apis/rank',params);
                // console.log('Rank:', response);
                this.novels = response.data;
                console.log('Novels:', this.novels);
            } catch (error) {
                console.error('Error fetching novel rank:', error);
            }
        }
    }
};
</script>

<style scoped>
.top{
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

</style>
</style>