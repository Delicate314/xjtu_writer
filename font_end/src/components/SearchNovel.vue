<template>
  <div class="search-container">
    <h2 class="link1">搜索小说</h2>
    <div class="search-form">
      <input type="text" placeholder="请输入搜索对象" v-model="query" @input="updateDisplay" @keyup.enter="search"
        class="rounded-input">
      <select v-model="queryType" class="rounded-select">
        <option v-for="(option, index) in searchOptions" :value="option.value" :key="index">{{ option.label }}</option>
      </select>
      <button class="rounded-button" @click="search">Search</button>
    </div>

    <div class="result-box">
      <div v-if="response.result.length > 0" class="result-list">
        <table>
          <thead>
            <tr>
              <th>小说标题</th>
              <th>作者名</th>
              <th>下载</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in response.result" :key="item.novel_id">
              <td>{{ item.novel_title }}</td>
              <td>{{ item.user_name }}</td>
              <td><button class="download-button"
                  @click="downloadNovel(item.novel_id, item.novel_title)">download</button></td>
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
  align-items: center;
  /* 垂直居中 */
}

.search-form {
  display: flex;
  align-items: center;
  /* 垂直居中 */
  margin-bottom: 20px;
  /* 底边距 */
}

.result-box {
  width: 100%;
  /* 宽度占满父容器 */
  max-height: 300px;
  /* 最大高度 */
  overflow-y: auto;
  /* 垂直滚动 */
  background-color: rgba(255, 255, 255, 0.8);
  /* 背景颜色及透明度 */
  border-radius: 10px;
  /* 圆角 */
  padding: 10px;
  /* 内边距 */
}

.result-list table {
  width: 100%;
  /* 表格宽度占满父容器 */
  border-collapse: collapse;
  /* 边框合并 */
}

.result-list th,
.result-list td {
  padding: 10px;
  /* 单元格内边距 */
  text-align: left;
  /* 文本左对齐 */
  border-bottom: 1px solid #ddd;
  /* 底部边框 */
}

.result-list th {
  background-color: #f2f2f2;
  /* 表头背景色 */
}

.download-button {
  padding: 5px 10px;
  /* 按钮内边距 */
  background-color: #007bff;
  /* 背景颜色 */
  color: #fff;
  /* 文字颜色 */
  border: none;
  /* 去除边框 */
  border-radius: 5px;
  /* 圆角 */
  cursor: pointer;
  /* 鼠标样式 */
}

.download-button:hover {
  background-color: #0056b3;
  /* 悬停时的背景颜色 */
}

.no-results {
  text-align: center;
  /* 文本居中 */
  color: #ffffff;
  /* 字体颜色 */
  font-size: 1.2em;
  /* 字体大小 */
  margin-top: 10px;
  margin-bottom: 10px;
}

input.rounded-input {
  padding: 13px 20px;
  margin-right: 10px;
  border-radius: 10px;
  border: 3px solid #112d4e;
  font-size: 15px;
}

select.rounded-select {
  padding: 10px 20px;
  margin-right: 10px;
  border-radius: 10px;
  border: 3px solid #112d4e;
  font-family: '微软雅黑';
  font-size: 15px;
  font-weight: 800;
}

button.rounded-button {
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

button.rounded-button:hover {
  background-color: #0056b3;
}


h2.link1 {
  font-size: 1.5em;
  /* 调整字体大小 */
  margin-bottom: 20px;
  /* 调整下边距 */
  color: #fff;
  /* 设置字体颜色 */
}

.result-box {
  background-color: rgba(255, 255, 255, 0.8);
  /* 设置背景颜色并添加透明度 */
  border-radius: 10px;
  /* 设置圆角 */
  padding: 10px;
  /* 设置内边距 */
  margin-top: 20px;
  /* 设置上边距 */
  text-align: left;
  /* 左对齐 */
  width: 300px;
  /* 设置较小的宽度 */
  margin: 0 auto;
  /* 使元素水平居中 */
}

.result-box ul {
  list-style: none;
  /* 去除列表样式 */
  padding: 0;
  /* 去除内边距 */
}

.result-box li {
  padding: 10px 0;
  /* 设置上下内边距 */
  border-bottom: 1px solid #000000;
  /* 设置下边框 */
}

.result-box li:last-child {
  border-bottom: none;
  /* 去除最后一个元素的下边框 */
}

.result-box p {
  margin: 0;
  /* 去除段落的默认外边距 */
  font-size: 1em;
  /* 调整字体大小 */
  color: #333;
  /* 设置字体颜色 */
}

@media (min-width: 600px) {

  /* Adjust for larger screens if needed */
  .search-form {
    flex-wrap: nowrap;
    /* Prevent wrapping on larger screens */
  }

  .result-box {
    width: 60%;
    /* Adjust width for larger screens */
    margin: 20px auto;
    /* Center align on larger screens */
  }
}
</style>