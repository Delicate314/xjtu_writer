<template>
    <div>
        <Background />
        <div class="top">
            <Guide_novel class="guide" />
        </div>
        <div class="novel-detail">
            <div class="png-aside">
                <img src="~@/assets/cover.png" alt="A Tale of Two Cities">
            </div>
            <div class="info">
                <h2 class="head">标题：{{ novel.novel_title }}</h2>
                <h3 class="footer">作者：{{ novel.writer_name }}</h3>
                <p class="footer">点击量：{{ novel.view_count }}</p>
                <p class="main">{{ novel.content }}</p>
                <textarea placeholder="向AI提问" v-model="question" class="footer_ask"></textarea>
                <button @click="ask" class='footer_commit'>提交</button>
                <textarea class="footer_answer" v-model="answer" readonly placeholder="生成的回答将在此显示"></textarea>
            </div>
        </div>
    </div>
</template>

<script>
import Background from '@/components/Background.vue';
import Guide_novel from '@/components/Guide_novel.vue';
import Guide from '@/components/Guide.vue';

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
        };
    },
    mounted() {
        this.getnovel();
    },
    methods: {
        async ask() {
            try {
                const requestData = {
                    question: this.question,  // 将问题添加到请求数据中
                    context: this.novel.content
                };
                console.log('Request Data:', requestData);
                const response = await this.$axios.post("http://121.36.55.149:80/apis/answer_request", requestData);
                console.log('Response:', response);
                this.answer = response.data;
            }
            catch (error) {
                console.error("Error generating text:", error);
                this.answer = "生成文本时出错，请稍后再试。";
            }
        },
        async getnovel() {
            console.log('Fetching novel data...');
            try {
                const params = {
                    novel_id: 1,
                    page: 1,
                    page_size: 2
                };

                const response = await this.$axios.post('http://121.36.55.149:80/apis/getNovel/', params);
                //console.log('Novel11111 data:', response);
                this.novel = response.data;
                console.log('Novel:', this.novel);
            } catch (error) {
                console.error('Error fetching novel data:', error);
            }
        }
    }
}
</script>

<style scoped>
.top {
    display: block;
    align-items: center;
    height: 50px;
    margin-top: 20px;
    margin-bottom: 20px;
}

.guide {
    color: red;
}

.novel-detail {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 20px;
    margin-top: 20px;
}

.png-aside {
    background-color: #D3DCE6;
    color: #333;
    text-align: center;
    height: 570px;
    width: 474px;
    /*wait for being changed*/
}

.head {
    font-family: "微软雅黑";
    font-weight: bold;
    background-color: #2b2e4a;
    color: #fff;
    text-align: center;
    line-height: 50px;
    width: 900px;
    height: 50px;
    margin: 0%;
    align-items: center;

    border: 2px solid #2b2e4a;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    font-size: 16px;
    resize: none;
    margin: 20px;
}

.footer {
    background-color: #903749;
    color: #fff;
    text-align: center;
    line-height: 50px;
    width: 900px;
    height: 50px;

    border: 2px solid #903749;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    font-size: 16px;
    resize: none;
    margin: 20px;
}

.main {
    background-color: #e84545;
    color: #fff;
    text-align: center;
    line-height: 40px;
    font-size: medium;
    width: 900px;

    order: 2px solid #e84545;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    font-size: 16px;
    resize: none;
    margin: 20px;
}

.info {
    text-align: center;
}

.footer_ask {
    display: block;
    width: 900px;
    height: 16px;
    padding: 10px;
    margin: 10px auto;
    background-color: #2b2e4a;
    color: #fff;
    margin-top: 10px;

    border: 2px solid #e84545;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    font-size: 16px;
    resize: none;
    margin: 20px;
}


.footer_commit {
    font-size: 20px;
    padding: 5px 20px;
    background-color: #2b2e4a;
    color: #fff;

    border: 2px solid #2b2e4a;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    font-size: 18px;
    resize: none;
}

.footer_answer {
    display: block;
    width: 900px;
    height: 90px;
    padding: 10px;
    margin: 10px auto;
    background-color: #2b2e4a;
    color: #fff;
    margin-top: 10px;

    border: 2px solid #e84545;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    font-size: 16px;
    resize: none;
    margin: 20px;
}
</style>