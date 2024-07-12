<template>
  <div>
    <Background />
    <div class="top">
      <Guide />
    </div>
    <textarea class="input-box" placeholder="演绎你的故事~,如:小明今天去扔垃圾,结果摔在了水坑里/一个勇者斗恶龙的故事" v-model="content"></textarea>
    <div>
      <button @click="write">创作</button>
      <button @click="upload">发布</button>
      <p v-if="write_isLoading" class="loading-text">
        请耐心等待... >.< <span class="loading-spinner"></span>
      </p>
    </div>
    <div>
      <textarea class="output-box" v-model="generatedContent" readonly placeholder="生成的文本将在此显示"></textarea>
    </div>
    <div>
      <textarea class="question-box" placeholder="请输入你的问题~" v-model="question"></textarea>
      <div>
        <button @click="answer">提问</button>
        <button @click="transit">转至输入</button>
        <p v-if="answer_isLoading" class="loading-text">
          请耐心等待... >.< <span class="loading-spinner"></span>
        </p>
      </div>
    </div>
    <div>
      <textarea class="output-box" v-model="answerContent" readonly placeholder="生成的回答将在此显示"></textarea>
    </div>
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
      question: '',  // 新增问题输入框数据
      write_isLoading: false, // 状态变量
      answer_isLoading: false,
    };
  },
  methods: {
    async write() {
      console.log('提交', this.content);
      this.write_isLoading = true; // 显示加载提示
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
        this.write_isLoading = false; // 隐藏加载提示
      }
    },
    async answer() {
      console.log('提交', this.question);
      this.answer_isLoading = true; // 显示加载提示
      try {
        const requestData = {
          question: this.question  // 将问题添加到请求数据中
        };
        console.log('Request Data:', requestData);

        const response = await axios.post("http://121.36.55.149:80/apis/answer_request", requestData);
        console.log('Response:', response);
        this.answerContent = response.data;
      }
      catch (error) {
        console.error("Error generating text:", error);
        if (error.response) {
          console.error("Response Data:", error.response.data);
          console.error("Response Status:", error.response.status);
          console.error("Response Headers:", error.response.headers);
        }
        this.generatedContent = "生成文本时出错，请稍后再试。";
      } finally {
        this.answer_isLoading = false; // 隐藏加载提示
      }
    },
    async upload() {
      console.log('上传', this.content);
      this.write_isLoading = true; // 显示加载提示
      try {
        const requestData = {
          contents: this.content,
        };
        console.log('Request Data:', requestData);

      }
      catch (error) {
        console.error("Error generating text:", error);
        if (error.response) {
          console.error("Response Data:", error.response.data);
          console.error("Response Status:", error.response.status);
          console.error("Response Headers:", error.response.headers);
        }
        this.generatedContent = "生成文本时出错，请稍后再试。";
      } finally {
        this.write_isLoading = false; // 隐藏加载提示
      }
    },
    transit() {
      this.content = this.generatedContent;
      this.generatedContent = '';
    },
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
  border: 2px solid #007bff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  font-size: 16px;
  resize: none;
  margin: 20px;
  background-color: rgba(255, 255, 255, 0.9);
  /* 设置文本框背景透明度 */
}

textarea.input-box {
  margin-bottom: 10px;
  /* 调整输入框之间的间距 */
  font-size: 20px;
}

textarea.question-box {
  width: 1200px;
  height: 20px;
  padding: 10px;
  border: 2px solid #007bff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  font-size: 20px;
  resize: none;
  margin-top: 10px;
  /* 问题输入框与提交按钮之间的间距 */
}

textarea.output-box {
  width: 1200px;
  /* 增大宽度 */
  height: 200px;
  /* 增大高度 */
  margin-top: 20px;
  background-color: rgba(255, 255, 255, 0.9);
  /* 设置文本框背景透明度 */
  cursor: not-allowed;
  font-size: 20px;
}

.button-container {
  display: flex;
  justify-content: center;
  margin-top: 10px;

}

/* 提交等按钮 */
button {
  padding: 10px 20px;
  background-color: #0088f7;
  color: #fff;
  border: none;
  cursor: pointer;
  border-radius: 20px;
  /* 圆角 */
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
  /* 将容器设为相对定位 */
  text-align: center;
  /* 右对齐文字和加载圈 */
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
  /* 将加载圈设为绝对定位 */
  top: 0%;
  /* 垂直居中 */
  left: 100%;
  /* 距离右侧边界 */
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
</style>