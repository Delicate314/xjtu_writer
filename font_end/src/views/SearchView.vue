<template>
  <div class="search_background">
    <h1 class="gradient-text">Welcome to XJTU AI-Writer! :)</h1>
    <router-link :key="index" :to="item.path" v-for="(item, index) in $router.options.routes">
      <span class="link" v-if="item.meta.isShow">{{ item.meta.name }}</span>
    </router-link>
    <h2 class="link1">搜索小说</h2>
      <input type="text" placeholder="请输入搜索对象" v-model="query" @input="updateDisplay" class="rounded-input">
      <select v-model="queryType" class="rounded-select">
        <option value="0">关键字</option>
        <option value="1">小说id</option>
        <option value="2">作者id</option>
      </select>
      <button class='search rounded-button' @click="search">Search</button>
      <div>{{ response }}</div>
    <h2 class="link1">上传文件</h2>
      <button @click="uploadFile" class='upload rounded-button'>上传文件</button>
      <input type="file" @change="handleFileUpload" />
    
  </div>
</template>

<script>
import StarryBackground from '../components/StarryBackground.vue';
import axios from 'axios';
export default {
  name: 'SearchView',
  components: {
    StarryBackground,
  },
  data() {
    return {
      query: '',
      queryType: '0', // 默认选择关键字
      displayText: '',
      response: [],
      selectedFile: null,
      type: 0
    };
  },
  methods: {
    async search() {
      event.preventDefault();
      console.log('Searching for', this.query, 'with type', this.queryType);
      const requestBody = {
        func: this.queryType,
        input: this.query
      };
      try {
        const response = await axios.post('http://121.36.55.149/apis/search', requestBody);
        console.log("response:", response);
        // 处理返回的响应数据
        this.response = response.data;
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
    updateDisplay(event) {
      // 更新要显示的文本
      this.displayText = event.target.value;
    },
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0];
    },
    // 上传文件到服务器
    uploadFile() {
      if (!this.selectedFile) {
        console.error('没有选择文件');
        return;
      }

      const formData = new FormData();
      formData.append('file', this.selectedFile);

      fetch('你的服务器端点', {
        method: 'POST',
        body: formData,
      })
        .then(response => response.json())
        .then(data => {
          console.log('文件上传成功', data);
          // 这里可以添加上传成功后的逻辑
        })
        .catch(error => {
          console.error('文件上传失败', error);
        });
    },
  },
};
</script>

<style>
.search_background {
  background-image: url('@/assets/search_background.jpg');
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
  height: 100vh;
  width: 100%;
  opacity: 1.0;
  position: relative;
  margin: 0px;
}

input.rounded-input,
select.rounded-select,
button.rounded-button {
  padding: 10px;
  margin-right: 10px;
  border-radius: 10px; /* 设置圆角 */
}

button.rounded-button {
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  cursor: pointer;
}

button.rounded-button:hover {
  background-color: #0056b3;
}

h2 {
  font-size: 1.5em; /* 调整字体大小 */
  margin-bottom: 20px; /* 调整下边距 */
  color: #007bff; /* 设置字体颜色 */
}


.link {
  text-decoration: none;
  top: 0;
  left: 0;
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

