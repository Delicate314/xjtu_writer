<template>
    <div class="search-container">
      <h2 class="link1">搜索小说</h2>
      <div class="search-form">
        <input type="text" placeholder="请输入搜索对象" v-model="query" @input="updateDisplay" @keyup.enter="search" class="rounded-input">
        <select v-model="queryType" class="rounded-select">
          <option v-for="(option, index) in searchOptions" :value="option.value" :key="index">{{ option.label }}</option>
        </select>
        <button class="search rounded-button" @click="search">Search</button>
      </div>
  
      <div class="result-box">
        <div v-if="response.result.length > 0" class="result-list">
          <table>
            <thead>
              <tr>
                <th>小说标题</th>
                <th>作者名</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in response.result" :key="item.novel_id">
                <td>{{ item.novel_title }}</td>
                <td>{{ item.user_name }}</td>
                <td><button class="download-button" @click="downloadNovel(item.novel_id, item.novel_title)">download</button></td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else class="no-results">
          <p>暂无结果</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'SearchNovel',
    data() {
      return {
        query: '',
        queryType: '0',
        response: {
          result: []
        },
        searchOptions: [
          { label: '关键字', value: '0' },
          { label: '小说id', value: '1' },
          { label: '作者id', value: '2' },
          { label: '作者名', value: '3' }
        ]
      };
    },
    methods: {
      async search() {
        event.preventDefault();
        console.log('Searching for', this.query, 'with type', this.queryType);
        const requestBody = {
          func: String(this.queryType),
          input: String(this.query)
        };
        try {
          const response = await axios.post('http://121.36.55.149/apis/search', requestBody);
          console.log("response:", response);
          this.response = response.data;
        } catch (error) {
          console.error("Error fetching data:", error);
        }
      },
      updateDisplay(event) {
        this.query = event.target.value;
      },
      async downloadNovel(nid, ntitle) {
        try {
          const requestData = { novel_id: String(nid) };
          const response = await axios.post("http://121.36.55.149/apis/downloadfile", requestData);
          if (response.status === 200) {
            const blob = new Blob([response.data], { type: 'text/plain' });
            const downloadUrl = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = downloadUrl;
            link.download = `${nid, ntitle}.txt`;
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
          this.$message.error('获取下载链接时发生错误');
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .search-container {
    display: flex;
    flex-direction: column;
    align-items: center; /* 垂直居中 */
  }
  
  .search-form {
    display: flex;
    align-items: center; /* 垂直居中 */
    margin-bottom: 20px; /* 底边距 */
  }
  
  .result-box {
    width: 100%; /* 宽度占满父容器 */
    max-height: 300px; /* 最大高度 */
    overflow-y: auto; /* 垂直滚动 */
    background-color: rgba(255, 255, 255, 0.8); /* 背景颜色及透明度 */
    border-radius: 10px; /* 圆角 */
    padding: 10px; /* 内边距 */
  }
  
  .result-list table {
    width: 100%; /* 表格宽度占满父容器 */
    border-collapse: collapse; /* 边框合并 */
  }
  
  .result-list th, .result-list td {
    padding: 10px; /* 单元格内边距 */
    text-align: left; /* 文本左对齐 */
    border-bottom: 1px solid #ddd; /* 底部边框 */
  }
  
  .result-list th {
    background-color: #f2f2f2; /* 表头背景色 */
  }
  
  .download-button {
    padding: 5px 10px; /* 按钮内边距 */
    background-color: #007bff; /* 背景颜色 */
    color: #fff; /* 文字颜色 */
    border: none; /* 去除边框 */
    border-radius: 5px; /* 圆角 */
    cursor: pointer; /* 鼠标样式 */
  }
  
  .download-button:hover {
    background-color: #0056b3; /* 悬停时的背景颜色 */
  }
  
  .no-results {
    text-align: center; /* 文本居中 */
    margin-top: 20px; /* 上边距 */
    color: #ffffff; /* 字体颜色 */
    font-size: 1.2em; /* 字体大小 */
  }
  </style>
  