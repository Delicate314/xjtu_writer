<template>
    <el-dialog :visible.sync="visible" title="小说内容" @close="handleClose" width="80%">
      <div v-if="loading">正在加载小说内容...</div>
      <div v-else-if="error">{{ error }}</div>
      <div v-else>
        <pre class="custom-text" v-html="formattedContent"></pre>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="downloadNovel" class="download-button">下载链接</el-button>
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
  computed: {
    formattedContent() {
      return this.novelContent.replace(/\n/g, '<br/>');
    }
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
    async fetchNovelContent() {
      this.loading = true;
      this.error = '';
      try {
        const requestData = {
          novel_id: this.novelId,
          page: 1,
          page_size: 100
        };
        const data = await axios.post("http://121.36.55.149/apis/getNovel", requestData);
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
        const requestData = {
          novel_id: String(this.novelId)
        };
        const response = await axios.post("http://121.36.55.149/apis/downloadfile", requestData);
        if (response.status === 200) {
          const blob = new Blob([response.data], { type: 'text/plain' });
          const downloadUrl = window.URL.createObjectURL(blob);
          const link = document.createElement('a');
          link.href = downloadUrl;
          link.download = `${this.novelName}.txt`;
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
          window.URL.revokeObjectURL(downloadUrl);
          this.$message.success('下载完成');
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
.custom-text {
  font-size: medium;
  white-space: pre-wrap;
  word-break: break-word;
  text-align: left;
  text-indent: 2em;
  line-height: 1.6; /* 设置行高，增加可读性 */
  padding: 10px; /* 增加内边距，防止文字贴边 */
  font-family: 'Microsoft YaHei', sans-serif; /* 设置字体 */
  color: #333; /* 设置文本颜色 */
}

.dialog-footer {
  display: flex;
  justify-content: center; /* 水平居中对齐 */
}

.download-button {
  max-width: 200px;
}
</style>
