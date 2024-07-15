<template>
    <div class="novels">
        <h2>我的小说</h2>
        <div class="novel-list">
            <table>
                <thead>
                    <tr>
                        <th>小说标题</th>
                        <th>浏览次数</th>
                        <th>更新时间</th>
                        <th>操作</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="novel in novels" :key="novel.novel_id">
                        <td>{{ novel.novel_title }}</td>
                        <td>{{ novel.novel_viewcount }}</td>
                        <td>{{ novel.UpdatedAt }}</td>
                        <td>
                            <router-link :to="`/Novel?id=${novel.novel_id}`" class="item-link">
                                <button @click="readNovel(novel.novel_id)" class="button read">阅读</button>
                            </router-link>
                            <!-- <button @click="editNovel(novel.novel_id)" class="button edit">修改</button> -->
                            <button @click="deleteNovel(novel.novel_id, novel.novel_title)"
                                class="button delete">删除</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            user_id: null,
            novels: [],
            novel_count: null,
        };
    },
    mounted() {
        this.fetchUserInfo();
    },
    methods: {
        async fetchUserInfo() {
            try {
                const { data } = await this.$axios.post("http://121.36.55.149:80/apis/user/ownInfo");
                this.novel_count = data.count;
                this.novels = data.novel;
                this.user_id = data.user_info.user_id;
            } catch (error) {
                console.error('An error occurred while fetching user information:', error);
            }
        },
        readNovel(novelId) {
            // 读取小说的逻辑
            console.log(`阅读小说: ${novelId}`);
        },
        editNovel(novelId) {
            // 修改小说的逻辑
            console.log(`修改小说: ${novelId}`);
        },
        async deleteNovel(novel_id, novel_title) {
            try {
                let response = await this.$axios.delete(`http://121.36.55.149:80/apis/user/deleteNovel?novel_id=${novel_id}&novel_title=${novel_title}`);
                console.log("返回信息：", response);
                this.fetchUserInfo();
            } catch (error) {
                console.error('删除小说时出错:', error);
            }
        },
    },
};
</script>

<style scoped>
.novels {
    background-color: #f5f5f5;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.novels h2 {
    font-size: 24px;
    color: #333;
    text-align: center;
    margin-bottom: 20px;
}

.novel-list {
    overflow-x: auto;
    /* 水平滚动 */
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 15px;
}

th,
td {
    padding: 10px;
    text-align: left;
    border-bottom: 1px solid #ddd;
}

th {
    background-color: #007bff;
    color: #fff;
}

tr:hover {
    background-color: #f2f2f2;
}

.button {
    padding: 8px 16px;
    font-size: 14px;
    color: #fff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

.button.read {
    background-color: #28a745;
}

.button.edit {
    background-color: #ffc107;
}

.button.delete {
    background-color: #dc3545;
}

.button:hover {
    opacity: 0.8;
}
</style>