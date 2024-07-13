<template>
    <el-dialog :visible.sync="visible" title="小说内容" @close="handleClose">
        <div v-if="loading">正在加载小说内容...</div>
        <div v-else-if="error">{{ error }}</div>
        <div v-else>
            <pre v-html="novelContent"></pre>
        </div>
        <span slot="footer" class="dialog-footer">
            <el-button type="primary" @click="downloadNovel">下载链接</el-button>
        </span>
    </el-dialog>
</template>

<script>
import axios from 'axios';
export default {
    props: {
        visible: {
            type: Boolean,
            required: true
        },
        novelId: {
            type: Number,
            required: true
        },
        novelName: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            novelContent: '',
            loading: false,
            error: '',
            url_api: '127.0.0.1:8000',
            url_serve: '121.36.55.149/apis'
        };
    },
    watch: {
        visible(newVal) {
            if (newVal) {
                this.fetchNovelContent();
            }
        }
    },
    methods: {
        handleClose() {
            this.$emit('update:visible', false);
        },
        fetchWithTimeout(url, options, timeout = 10000) {
            return Promise.race([
                fetch(url, options),
                new Promise((_, reject) =>
                    setTimeout(() => reject(new Error('请求超时')), timeout)
                )
            ]);
        },
        async fetchNovelContent() {
            this.loading = true;
            this.error = '';
            try {
                const requestData = {
                    novel_id: this.novelId,
                    page: 1,
                    page_size: 10
                };
                console.log('Request Data:', requestData);
                const data = await axios.post("http://121.36.55.149/apis/getNovel", requestData);
                console.log('Response:', data);
                // const response = await this.fetchWithTimeout(
                // 'http://121.36.55.149/apis/getNovel',
                // {
                //     method: 'POST',
                //     headers: {
                //         'Accept': 'application/json',
                //         'Content-Type': 'application/json'
                //     },
                //     body: JSON.stringify({
                //         novel_id: this.novelId,
                //         page: 1,
                //         page_size: 10
                //     })
                // }
                // );
                // const data = await response.json();
                if (data.data.content) {
                    this.novelContent = data.data.content;
                } else {
                    this.error = '获取小说内容失败';
                }
            } catch (error) {
                console.error('Error fetching novel content:', error);
                this.error = '获取小说内容时发生错误';
            } finally {
                this.loading = false;
            }
        },
        async downloadNovel() {
            try {
                const response = await this.fetchWithTimeout(
                    'http://121.36.55.149/apis/downloadfile',
                    {
                        method: 'POST',
                        headers: {
                            'Accept': 'application/json',
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            novel_id: String(this.novelId)
                        })
                    }
                );
                if (response.status === 200) {
                    const blob = await response.blob();
                    const downloadUrl = window.URL.createObjectURL(blob);
                    const link = document.createElement('a');
                    link.href = downloadUrl;
                    link.download = `${this.novelName}.txt`;
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                    window.URL.revokeObjectURL(downloadUrl);
                } else {
                    this.error = '获取下载链接失败';
                }
            } catch (error) {
                console.error('Error fetching download link:', error);
                this.error = '获取下载链接时发生错误';
            }
        }
    }
};
</script>

<style scoped>
pre {
    white-space: pre-wrap;
    word-break: break-word;
    /* 可选，增加此行以在长单词或URL时也进行换行 */
    text-align: left;
    /* 左对齐 */
    text-indent: 2em;
    /* 首行缩进两个字符长度 */
}
</style>
