<template>
  <div>
    <Background />
    <div class="top">
      <Guide />
    </div>
    <textarea class="input-box" placeholder="演绎你的故事(๑•́ ₃ •̀๑)ｴｰ,如:小明今天去扔垃圾,结果摔在了水坑里/一个勇者斗恶龙的故事"
      v-model="content"></textarea>
    <div>
      <button @click="clear">清空输入</button>
      <button @click="write">AI创作</button>
      <button @click="import_novel">导入本地文章</button>
      <input type="file" ref="fileInput" @change="handleFileChange" style="display: none;">
      <p v-if="write_isLoading" class="loading-text">
        AI努力创作中,请耐心等待... >.< <span class="loading-spinner"></span>
      </p>
    </div>
    <div>
      <textarea class="output-box" v-model="generatedContent" readonly placeholder="生成的文章将在此显示(o´∀`o)"></textarea>
    </div>
    <div>
      <textarea class="question-box" placeholder="针对上面的文章，输入你的问题~" v-model="question"></textarea>
      <div>
        <button @click="mergeInputToGenerated">合并续写文章</button>
        <button @click="showUploadDialog">发布到社区</button>
        <button @click="answer">提问</button>
        <button @click="transit">将生成文本转至输入</button>
        <p v-if="answer_isLoading" class="loading-text">
          请耐心等待... >.< <span class="loading-spinner"></span>
        </p>
      </div>
    </div>
    <div>
      <textarea class="output-box" v-model="answerContent" readonly placeholder="生成的回答将在此显示(o´∀`o)"></textarea>
    </div>

    <!-- Element UI Dialog for Title Input -->
    <el-dialog title="给文章起一个标题吧٩(๑`^´๑)۶" :visible.sync="dialogVisible" width="30%" @close="handleClose">
      <el-input v-model="novel_title" placeholder="请输入标题"></el-input>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="upload">确认</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios';
import Guide from '@/components/Guide.vue';
import Background from '@/components/Background.vue';

export default {
  name: 'WriteView',
  components: {
    Guide,
    Background,
  },
  data() {
    return {
      content: '',
      generatedContent: '',
      answerContent: '',
      question: '',
      write_isLoading: false,
      answer_isLoading: false,
      novel_title: '',
      dialogVisible: false,
    };
  },
  methods: {
    async write() {
      if (this.content.trim() === '') {
        this.$message.error('输入不能为空');
        return;
      }
      console.log('提交', this.content);
      this.write_isLoading = true;
      try {
        const requestData = {
          contents: this.content,
        };
        console.log('Request Data:', requestData);

        const response = await axios.post("http://121.36.55.149:80/apis/write_request", requestData);
        console.log('Response:', response);

        this.generatedContent = response.data;
        console.log('Generated Text:', this.generatedContent);
      } catch (error) {
        console.error("Error generating text:", error);
        if (error.response) {
          console.error("Response Data:", error.response.data);
          console.error("Response Status:", error.response.status);
          console.error("Response Headers:", error.response.headers);
        }
        this.generatedContent = "生成文本时出错，请稍后再试。";
      } finally {
        this.write_isLoading = false;
      }
    },
    async answer() {
      console.log('提问', this.question);
      this.answer_isLoading = true;
      try {
        const requestData = {
          question: this.question,
          context: this.generatedContent
        };
        console.log('Request Data:', requestData);

        const response = await axios.post("http://121.36.55.149:80/apis/answer_request", requestData);
        console.log('Response:', response);
        this.answerContent = response.data;
        this.answer_isLoading = false;
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
    showUploadDialog() {
      this.dialogVisible = true;
    },
    handleClose() {
      this.dialogVisible = false;
      this.novel_title = '';
    },
    async upload() {
      if (!this.novel_title.trim()) {
        this.$message.error('标题不能为空');
        return;
      }
      console.log('发布');
      const formData = new FormData();
      formData.append('novel', this.generatedContent);
      formData.append('novel_title', this.novel_title);
      try {
        const response = await axios.post('http://121.36.55.149/apis/novel/releaseNovel', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        // 这里可以添加上传成功后的逻辑
        this.$message.success('发布成功');
        this.dialogVisible = false;
      }
      catch (error) {
        console.error('发布失败', error);
        alert('发布失败，请重试');
      }
    },
    transit() {
      this.content = this.generatedContent;
      this.generatedContent = '';
    },
    clear() {
      this.content = '';
    },
    import_novel() {
      this.$refs.fileInput.click();
    },
    handleFileChange(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.content = e.target.result;
        };
        reader.readAsText(file);
      }
    },
    mergeInputToGenerated() {
      if (this.content.trim() === '') {
        this.$message.error('输入文本框为空');
        return;
      }
      else if (this.generatedContent === '') {
        this.$message.error('生成文本框为空');
        return;
      }
      this.generatedContent = this.content + '\n\n' + this.generatedContent;
      this.content = ''; // Clear input after merging
    }
  },
};
</script>

<style scoped>
.top {
  margin-top: 20px;
}

textarea {
  width: 1200px;
  height: 150px;
  padding: 10px;
  margin-top: 10px;
  border: 2px solid #14668193;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  font-size: 16px;
  resize: none;
  margin: 20px auto;
  background-color: rgba(255, 255, 255, 0.9);
}

textarea.input-box {
  margin-bottom: 10px;
  font-size: 20px;
}

textarea.question-box {
  width: 1200px;
  height: 20px;
  padding: 10px;
  border: 2px solid #14668193;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  font-size: 20px;
  resize: none;
  margin-top: 10px;
}

textarea.output-box {
  width: 1200px;
  height: 200px;
  margin-top: 20px;
  background-color: rgba(255, 255, 255, 0.9);
  cursor: not-allowed;
  font-size: 20px;
}

.button-container {
  display: flex;
  justify-content: center;
  margin-top: 10px;
}

button {
  padding: 10px 20px;
  background-color: #0088f7;
  color: #fff;
  border: none;
  cursor: pointer;
  border-radius: 20px;
  box-shadow: 0 4px 8px rgba(6, 0, 125, 0.1);
  transition: background-color 0.8s ease, box-shadow 0.3s ease;
  margin: 0 10px;
  font-weight: bold;
  font-size: 18px;
}

button:hover {
  background-color: #1667f3;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
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

/* Add media queries for smaller screens */
@media (max-width: 768px) {
  textarea {
    width: 85%;
    font-size: 14px;
  }

  button {
    width: 50%;
    margin: 10px 0;
    font-size: 16px;
  }

  textarea.input-box,
  textarea.question-box,
  textarea.output-box {
    height: 100px;
    width: 85%;
  }

  textarea.output-box {
    height: 150px;
  }
}
</style>
