<template>
    <div class="novels" v-loading="loading">
        <h2>我的小说</h2>
        <div v-if="novel_count === 0" class="no-novels-message">
            你还没有小说哦，去搜索页面上传或者写小说页面创作后发布吧ヽ(・∀・)ﾉ！！！
        </div>
        <div v-else class="novel-list">
            <table>
                <thead>
                    <tr>
                        <th class="rank-top">小说标题</th>
                        <th>热度</th>
                        <th class="rank-bottom">操作</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="novel in novels" :key="novel.novel_id">
                        <td>{{ novel.novel_title }}</td>
                        <td>
                            <div class="el-rate-container">
                                <el-rate v-model="novel.rating" disabled show-score text-color="#ff9900" :max="5"
                                    class="mobile-el-rate" />
                            </div>
                        </td>
                        <td>
                            <router-link :to="`/Novel?id=${novel.novel_id}`" class="item-link">
                                <el-button type="success" size="small" class="button read"
                                    @click="readNovel(novel.novel_id)">
                                    阅读
                                </el-button>
                            </router-link>
                            <el-popconfirm popper-class="my-popconfirm" confirm-button-text="确定" cancel-button-text="取消"
                                icon="el-icon-delete" icon-color="red" title="此操作无法撤销，确定删除该小说？"
                                @confirm="deleteNovel(novel.novel_id, novel.novel_title)">
                                <el-button slot="reference" type="danger" size="small" class="button delete">
                                    删除
                                </el-button>
                            </el-popconfirm>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import { MessageBox } from 'element-ui';
export default {
    data() {
        return {
            user_id: null,
            novels: [],
            novel_count: null,
            loading: true,
        };
    },
    mounted() {
        this.fetchUserInfo();
    },
    methods: {
        async fetchUserInfo() {
            try {
                this.loading = true;
                const { data } = await this.$axios.post("http://121.36.55.149:80/apis/user/ownInfo");
                this.novel_count = data.count;
                this.novels = data.novel.map(novel => ({
                    ...novel,
                    rating: Math.min(Math.floor(novel.novel_viewcount / 200 * 10) / 10, 5)
                }));
                this.user_id = data.user_info.user_id;
                this.loading = false;
            } catch (error) {
                console.error('An error occurred while fetching user information:', error);
            }
        },
        readNovel(novelId) {
            // 读取小说的逻辑
            console.log(`阅读小说: ${novelId}`);
        },
        async deleteNovel(novel_id, novel_title) {
            try {
                this.loading = true;
                let response = await this.$axios.delete(`http://121.36.55.149:80/apis/user/deleteNovel?novel_id=${novel_id}&novel_title=${novel_title}`);
                this.$message.success('文件上传成功');
                console.log("返回信息：", response);
                this.fetchUserInfo();
            } catch (error) {
                console.error('删除小说时出错:', error);
                MessageBox.alert(`删除小说时出错，请稍后再试>.<`, '错误', {
                    confirmButtonText: '确定',
                    type: 'error',
                });
            }
        },
    },
};
</script>

<style scoped>
.novels {
    background-color: #f5f5f5;
    padding: 10px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    width: 90%;
    margin: 0 auto;
    /* 将容器居中 */
}

.novels h2 {
    font-size: 24px;
    color: #333;
    text-align: center;
    margin-bottom: 20px;
}

.no-novels-message {
    text-align: center;
    font-size: 18px;
    color: #666;
}

.novel-list {
    overflow: hidden;
}

.rank-top {
    border-top-left-radius: 8px;
    border-bottom-left-radius: 8px;
}

.rank-bottom {
    border-top-right-radius: 8px;
    border-bottom-right-radius: 8px;
}

table {
    width: 100%;
    border-collapse: collapse;
    table-layout: fixed;
    /* 固定表格布局 */
}

thead th {
    padding: 10px;
    background-color: #007bff;
    color: #fff;
    text-align: left;
}

tbody {
    display: block;
    max-height: 350px;
    overflow-y: auto;
}

tbody tr {
    display: table;
    width: 100%;
    table-layout: fixed;
}

thead,
tbody tr {
    display: table;
    width: 100%;
    table-layout: fixed;
}

tbody td {
    padding: 10px;
    text-align: left;
    border-bottom: 1px solid #ddd;
}

tbody tr:hover {
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
    background-color: #67c23a;
}

.button.edit {
    background-color: #ffc107;
}

.button.delete {
    background-color: #f56c6c;
}

.button:hover {
    opacity: 0.8;
}

/* Adjustments for el-rate component */
.mobile-el-rate {
    font-size: 14px;
    /* Adjust font size */
}

.el-rate-container {
    display: flex;
    align-items: center;
    /* Center align the el-rate */
}
</style>