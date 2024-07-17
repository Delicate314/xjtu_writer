<template>
    <div>
        <Background />
        <div class="top">
            <Guide_novel class="guide" />
        </div>
        <div class="novel-detail-container" :class="{ 'shifted': showAISection }">
            <div class="novel-detail-left">
                <div class="info" v-loading="novelLoading">
                    <h2 class="head">标题：{{ novel.novel_title }}</h2>
                    <h3 class="footer">作者：{{ novel.writer_name }}</h3>
                    <h3>热度</h3>
                    <el-rate v-model="rating" disabled show-score text-color="#ff9900" :score-template="`{value}`">
                    </el-rate>
                    <textarea ref="novelTestarea" readonly class="main" :value="formattedContent"></textarea>
                </div>
                <div class="pagination">
                    <button @click="prevPage" :disabled="page === 1">上一页</button>
                    <button @click="nextPage">下一页</button>
                    <label for="pageSize">每页显示:</label>
                    <input type="number" v-model.number="pageSize" @change="updatePageSize" min="1" id="pageSize" />
                    <button @click="toggleAISection" class="toggle-button">
                        {{ showAISection ? '隐藏提问和评论框' : '显示提问和评论框' }}
                    </button>
                </div>
            </div>
            <div class="novel-detail-right" v-if="showAISection">
                <textarea placeholder="针对文章内容向AI提问" v-model="question" class="footer_ask"></textarea>
                <button @click="ask" class="footer_commit">提问</button>
                <p v-if="answer_isLoading" class="loading-text">
                    请耐心等待... >.< <span class="loading-spinner"></span>
                </p>
                <textarea class="footer_answer" v-model="answer" readonly placeholder="生成的回答将在此显示"></textarea>
                <div class="comments-section" v-loading="commentLoading">
                    <h3>评论</h3>
                    <el-input v-model="newComment" placeholder="输入评论" class="comment"></el-input>
                    <el-button @click="submitComment" class="footer_commit">评论</el-button>

                    <!-- Comments loop -->
                    <div v-for="(item, index) in formattedComments" :key="index" class="comment">
                        <div class="author-info">
                            <span class="author-name">{{ item.username }}</span>
                            <span class="author-time">{{ item.formattedUpdatedAt }}</span>
                        </div>
                        <textarea class="comment-content" readonly>{{ item.comment_content }}</textarea>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Background from '@/components/Background.vue';
import Guide_novel from '@/components/Guide_novel.vue';
import Guide from '@/components/Guide.vue';
import axios from 'axios';
import { ElInput, ElButton, ElRate } from 'element-ui';

export default {
    name: 'NovelDetail',
    components: {
        Guide_novel,
        Background,
        Guide,
    },
    data() {
        return {
            novelLoading: true,
            commentLoading: true,
            novel: {},
            question: '',
            answer: '',
            page: 1,
            pageSize: 15,
            showAISection: true,
            answer_isLoading: false, // Track loading state
            rating: 0.0, // Rating for novel
            comments: [], // Make sure comments is an array
            newComment: '', // New comment content
        };
    },
    mounted() {
        this.getNovel();
        this.getComment();
    },
    computed: {
        formattedContent() {
            if (this.novel.content) {
                return this.novel.content.replace(/<br\s*\/?>/gi, '\n');
            }
            else {
                return this.novel.content;
            }
        },
        formattedComments() {
            return this.comments.map(comment => {
                return {
                    ...comment,
                    formattedUpdatedAt: comment.UpdatedAt.replace('T', ' ')
                };
            });
        }
    },
    methods: {
        async ask() {
            console.log('提问', this.question);
            this.answer_isLoading = true;
            this.answer = ''; // Clear previous answer
            try {
                const requestData = {
                    question: this.question,
                    context: this.novel.content
                };
                console.log('Request Data:', requestData);

                const response = await axios.post("http://121.36.55.149:80/apis/answer_request", requestData);
                console.log('Response:', response);
                this.answer = response.data;
            }
            catch (error) {
                console.error("Error generating text:", error);
                if (error.response) {
                    console.error("Response Data:", error.response.data);
                    console.error("Response Status:", error.response.status);
                    console.error("Response Headers:", error.response.headers);
                    alert("网络错误，请重试");
                }
                alert("输入文本太大,请尝试减小每页显示的字数再提问。QAQ");
            }
            finally {
                this.answer_isLoading = false;
            }
        },
        async getNovel() {
            this.novelLoading = true;
            console.log('Fetching novel data...');
            try {
                const params = {
                    novel_id: Number(this.$route.query.id),
                    page: this.page,
                    page_size: this.pageSize
                };
                const response = await this.$axios.post('http://121.36.55.149:80/apis/getNovel/', params);
                this.novel = response.data;
                console.log('Novel:', this.novel);

                // Calculate rating based on view count
                this.rating = Math.min(Math.floor(this.novel.view_count / 200 * 10) / 10, 5); // 将计算结果保留一位小数，并限制最大为 5
                this.novelLoading = false;
            } catch (error) {
                console.error('Error fetching novel data:', error);
            }
        },

        async getComment() {
            this.commentLoading = true;
            console.log('Fetching novel comments...');
            const formData = new FormData();
            console.log(formData);
            console.log(this.$route.query.id);
            formData.append('novel_id', Number(this.$route.query.id));
            console.log("formdata", formData);
            try {
                const response2 = await this.$axios.post('http://121.36.55.149:80/apis/comment/getcomments', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                });
                console.log('comments', response2.data);
                this.comments = response2.data.comments;
                // 这里可以添加上传成功后的逻辑
                this.commentLoading = false;
            } catch (error) {
                console.error('文件上传失败', error);
            }
        },
        async submitComment() {
            console.log('Submitting comment...');
            try {
                // Sensitive words filter
                const sensitiveWords = ['傻逼', 'fuck', 'FUCK', '草你妈', '色情', '毒品', '自杀']; // Add your sensitive words here

                // Check if newComment contains sensitive words
                for (let word of sensitiveWords) {
                    if (this.newComment.includes(word)) {
                        this.$message.error('评论包含敏感词汇，请修改后重新提交');
                        return; // Prevent comment submission
                    }
                }

                const formData = new FormData();
                formData.append('novel_id', Number(this.$route.query.id));
                formData.append('comment_content', this.newComment);
                console.log("formdata", formData);
                const response = await this.$axios.post('http://121.36.55.149:80/apis/comment/uploadcomment', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                });
                console.log('Comment submitted:', response.data);
                this.newComment = ''; // Clear the input field
                this.$message.success('评论发布成功');
                this.getComment(); // Refresh the comments
            } catch (error) {
                console.error('Error submitting comment:', error);
            }
        },
        nextPage() {
            this.page++;
            this.getNovel();
            this.$nextTick(() => {
                this.$refs.novelTestarea.scrollTop = 0;
            });
        },
        prevPage() {
            if (this.page > 1) {
                this.page--;
                this.getNovel();
                this.$nextTick(() => {
                    this.$refs.novelTestarea.scrollTop = 0;
                });
            }
        },
        updatePageSize() {
            this.page = 1;
            this.getNovel();
        },
        toggleAISection() {
            this.showAISection = !this.showAISection;
        }
    }
};
</script>

<style scoped>
body {
    font-family: 'Arial', sans-serif;
    background-color: #f0f0f0;
    color: #333;
    margin: 0;
    padding: 0;
}

.novel-detail-container {
    display: block;
    justify-content: center;
    margin: 30px;
    background: #fff;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    padding: 20px;
    transition: all 0.3s ease;
}

.novel-detail-container.shifted {
    justify-content: space-between;
}

.novel-detail-left {
    flex: 3;
    margin-right: 20px;
    transition: margin-right 0.3s ease;
}

.novel-detail-right {
    flex: 1;
    transition: opacity 0.3s ease;
    opacity: 0;
    pointer-events: none;
}

.novel-detail-container.shifted .novel-detail-left {
    margin-right: 0;
}

.novel-detail-container.shifted .novel-detail-right {
    opacity: 1;
    pointer-events: auto;
}

.info {
    margin-bottom: 20px;
}

.head,
.footer {
    margin: 10px 0;
    color: #333;
}

.head {
    font-size: 1.5em;
    font-weight: bold;
}

.footer {
    font-size: 1em;
    color: #666;
}

.main {
    width: 99%;
    height: 450px;
    margin: 10px 0;
    padding: 10px;
    border-radius: 8px;
    border: 1px solid #ccc;
    font-family: 'Arial', sans-serif;
    font-size: 18px;
    resize: vertical;
}

.footer_ask,
.footer_answer,
.comments-section textarea {
    font-size: 18px;
    width: 99%;
    margin: 10px auto;
    padding: 10px;
    border-radius: 8px;
    border: 1px solid #ccc;
    font-family: 'Arial', sans-serif;
    resize: vertical;
}

.footer_commit {
    display: block;
    width: 20%;
    padding: 10px;
    margin: 10px 0;
    margin-left: auto;
    margin-right: 0px;
    /* 添加这行 */
    border: none;
    border-radius: 8px;
    background-color: #007bff;
    color: white;
    font-size: 16px;
    cursor: pointer;
    resize: vertical;
}

.footer_commit:hover {
    background-color: #0056b3;
}

.footer_answer {
    height: 150px;
}


.pagination {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 20px;
}

.pagination button {
    padding: 10px 15px;
    border-radius: 5px;
    border: 1px solid #ccc;
    background: #fff;
    cursor: pointer;
    transition: background 0.3s;
}

.pagination button:hover {
    background: #f0f0f0;
}

.pagination input {
    width: 60px;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #ccc;
    text-align: center;
}

.toggle-button {
    display: block;
    margin: 20px 0;
    padding: 10px 20px;
    border: none;
    border-radius: 8px;
    background-color: #28a745;
    color: #000000;
    font-size: 16px;
    cursor: pointer;
    transition: background 0.3s;
    margin-left: 20px;
}

.toggle-button:hover {
    background-color: #e3a704;
}

.loading-text {
    position: relative;
    text-align: center;
    color: #ffffff;
    font-size: 20px;
    margin-top: 10px;
    font-family: 'Comic Sans MS', cursive, sans-serif;
    text-shadow: 1px 1px 2px #888888;
}

.loading-spinner {
    border: 4px solid rgba(0, 0, 0, 0.1);
    border-top: 4px solid #ffffff;
    border-radius: 50%;
    width: 20px;
    height: 20px;
    animation: spin 1s linear infinite;
    position: absolute;
    top: 0%;
    left: 100%;
    transform: translate(-50%, -50%);
}


@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}

.comment {
    border-top: 1px solid #eee;
    padding: 10px 0;
    min-height: 40px;
    resize: vertical;
    font-size: 18px;
}



.author-info {
    display: flex;
    align-items: center;
    margin-bottom: 5px;
    /* Adjust margin as needed */
}

.author-info>span {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin-right: 10px;
    /* Adjust spacing between name and time */
}

.author-name {
    color: #000;
    font-size: 16px;
    font-weight: bold;
}

.author-time {
    color: #666;
    font-size: 14px;
}

.comment-content {
    width: 100%;
    min-height: 100px;
    /* Adjust minimum height as needed */
    margin-top: 5px;
    /* Adjust margin top as needed */
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 5px;
    resize: vertical;
    /* Prevent resizing */
}

/* Ensure the spinner is positioned properly within the loading text */
.loading-text {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
}

/* Add media query for smaller screens */
@media (max-width: 768px) {

    .main,
    .footer_ask,
    .footer_answer,
    .comments-section textarea {
        margin-left: 10px;
        /* Adjust the left margin as per your design */
        margin-right: 20px;
        /* Adjust the right margin as per your design */
    }
}
</style>
