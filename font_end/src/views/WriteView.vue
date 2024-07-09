<template>
  <div>
    <router-link :key="index" :to="item.path" v-for="(item, index) in $router.options.routes">
      <span class="link" v-if="item.meta.isShow">{{ item.meta.name }}</span>
    </router-link>
    <h2>XJTU AI-Writer</h2>
    <textarea class="input-box" placeholder="续写你的小说~" v-model="content"></textarea>
    <textarea class="question-box" placeholder="请输入你的问题~" v-model="question"></textarea>
    <div class="button-container">
      <button @click="write">续写</button>
      <button @click="answer">提问</button>
    </div>
    <p v-if="isLoading" class="loading-text">请耐心等待...</p>
    <textarea class="output-box" v-model="generatedContent" readonly placeholder="生成的文本将在此显示"></textarea>
    <textarea class="output-box" v-model="answerContent" readonly placeholder="生成的文本将在此显示"></textarea>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'WriteView',
  data() {
    return {
      content: '',
      generatedContent: '',
      answerContent: '',
      question: '',  // 新增问题输入框数据
      isLoading: false, // 状态变量
    };
  },
  methods: {
    async write() {
      console.log('提交', this.content);
      this.isLoading = true; // 显示加载提示
      try {
        const requestData = {
          contents: this.content,
        };
        console.log('Request Data:', requestData);

        const response = await axios.post("http://127.0.0.1:8000/apis/write_request", requestData);
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
        this.isLoading = false; // 隐藏加载提示
      }
    },
    async answer() {
      console.log('提交', this.question);
      this.isLoading = true; // 显示加载提示
      try {
        const requestData = {
          question: this.question  // 将问题添加到请求数据中
        };
        console.log('Request Data:', requestData);

        const response = await axios.post("http://127.0.0.1:8000/apis/answer_request", requestData);
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
        this.isLoading = false; // 隐藏加载提示
      }
    },
  },
};
</script>

<style>
textarea {
  width: 300px;
  height: 150px;
  padding: 10px;
  margin-top: 10px;
  border: 2px solid #007bff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  font-size: 16px;
  resize: none;
}

textarea.input-box {
  margin-bottom: 10px;
  /* 调整输入框之间的间距 */
}

textarea.question-box {
  width: 300px;
  height: 100px;
  padding: 10px;
  border: 2px solid #007bff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  font-size: 16px;
  resize: none;
  margin-top: 10px;
  /* 问题输入框与提交按钮之间的间距 */
}

textarea.output-box {
  width: 400px;
  /* 增大宽度 */
  height: 200px;
  /* 增大高度 */
  margin-top: 20px;
  background-color: #f5f5f5;
  cursor: not-allowed;
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
  /* 圆角 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
  margin: 0 10px;
}

button:hover {
  background-color: #1f72f7;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

.loading-text {
  text-align: center;
  color: #ff0000;
  font-size: 16px;
  margin-top: 10px;
}

.link {
  text-decoration: none;
  color: #007bff;
  margin: 0 10px;
  padding: 5px 10px;
  border: 2px solid #007bff;
  border-radius: 15px;
  display: inline-block;
  transition: all 0.3s ease;
  position: relative;
}

.link:hover {
  color: #fff;
  background-color: #007bff;
  animation: jelly 0.5s;
}
</style>
