<template>
    <div>
        <Background />
        <div class="top">
            <Guide_novel class="guide" />
        </div>
        <div class="novel-detail-container" :class="{ 'shifted': showAISection }">
            <div class="novel-detail-left">
                <div class="info">
                    <h2 class="head">标题：{{ novel.novel_title }}</h2>
                    <h3 class="footer">作者：{{ novel.writer_name }}</h3>
                    <p class="footer">点击量：{{ novel.view_count }}</p>
                    <textarea class="main" :value="formattedContent"></textarea>
                </div>
                <div class="pagination">
                    <button @click="prevPage" :disabled="page === 1">上一页</button>
                    <button @click="nextPage">下一页</button>
                    <label for="pageSize">每页显示:</label>
                    <input type="number" v-model.number="pageSize" @change="updatePageSize" min="1" id="pageSize" />
                    <button @click="toggleAISection" class="toggle-button">
                        {{ showAISection ? '隐藏AI提问' : '显示AI提问' }}
                    </button>
                </div>
            </div>
            <div class="novel-detail-right" v-if="showAISection">
                <textarea placeholder="针对文章内容向AI提问" v-model="question" class="footer_ask"></textarea>
                <button @click="ask" class='footer_commit'>提问</button>
                <textarea class="footer_answer" v-model="answer" readonly placeholder="生成的回答将在此显示"></textarea>
            </div>
        </div>
    </div>
</template>

<script>
import Background from '@/components/Background.vue';
import Guide_novel from '@/components/Guide_novel.vue';
import Guide from '@/components/Guide.vue';
import axios from 'axios';

export default {
    name: 'NovelDetail',
    components: {
        Guide_novel,
        Background,
        Guide,
    },
    data() {
        return {
            novel: {},
            question: '',
            answer: '',
            page: 1,
            pageSize: 50,
            showAISection: false
        };
    },
    mounted() {
        this.getnovel();
    },
    computed: {
        formattedContent() {
            return this.novel.content.replace(/<br\s*\/?>/gi, '\n');
        }
    },
    methods: {
        async ask() {
            console.log('提问', this.question);
            this.answer_isLoading = true;
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
                }
                alert("网络出错，请稍后再试。");
            }
        },
        async getnovel() {
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
            } catch (error) {
                console.error('Error fetching novel data:', error);
            }
        },
        nextPage() {
            this.page++;
            this.getnovel();
        },
        prevPage() {
            if (this.page > 1) {
                this.page--;
                this.getnovel();
            }
        },
        updatePageSize() {
            this.page = 1;
            this.getnovel();
        },
        toggleAISection() {
            this.showAISection = !this.showAISection;
        }
    }
}
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
    /* 添加过渡效果 */
}

.novel-detail-right {
    flex: 1;
    transition: opacity 0.3s ease;
    /* 添加过渡效果 */
    opacity: 0;
    /* 默认隐藏 */
    pointer-events: none;
    /* 默认不可交互 */
}

.novel-detail-container.shifted .novel-detail-left {
    margin-right: 0;
}

.novel-detail-container.shifted .novel-detail-right {
    opacity: 1;
    /* 显示AI部分 */
    pointer-events: auto;
    /* 可交互 */
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
    width: 100%;
    height: 450px;
    margin: 10px 0;
    padding: 10px;
    border-radius: 8px;
    border: 1px solid #ccc;
    font-family: 'Arial', sans-serif;
    font-size: 18px;
}

.footer_ask,
.footer_answer {
    width: 100%;
    height: 100px;
    margin: 10px 0;
    padding: 10px;
    border-radius: 8px;
    border: 1px solid #ccc;
    font-family: 'Arial', sans-serif;
}

.footer_commit {
    display: block;
    width: 100%;
    padding: 10px;
    margin: 10px 0;
    border: none;
    border-radius: 8px;
    background-color: #007bff;
    color: white;
    font-size: 16px;
    cursor: pointer;
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
</style>
