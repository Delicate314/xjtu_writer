<template>
  <div class="top">
    <Background />
    <Guide />
    <h2 class="link1">搜索小说</h2>
    <input type="text" placeholder="请输入搜索对象" v-model="query" @input="updateDisplay" class="rounded-input">
    <select v-model="queryType" class="rounded-select">
      <option v-for="(option, index) in searchOptions" :value="index" :key="index">{{ option.label }}</option>
    </select>
    <button class="search rounded-button" @click="search">Search</button>
    <div v-if="response.result.length > 0" class="result-box">
      <h3>搜索结果：</h3>
      <ul>
        <li v-for="item in response.result" :key="item.novel_id">
          <p>
            {{ item.novel_title }} - {{ item.user_name }}
            <button class="search rounded-button" @click="download(item.novel_id, item.novel_title)">download</button>
          </p>
        </li>
      </ul>
    </div>
    <div v-else>
      <p>暂无结果</p>
    </div>
    <h2 class="link1">上传文件</h2>
    <input type="file" @change="handleFileUpload" />
    <div v-if="selectedFile" class="file-info">
      <p>已选择文件：{{ selectedFile.name }}</p>
    </div>
    <button @click="uploadFile" class="upload rounded-button">上传文件</button>
  </div>
</template>

<script>
import StarryBackground from '../components/StarryBackground.vue';
import axios from 'axios';
import Background from '../components/Background.vue';
import Guide from '../components/Guide.vue';

export default {
  name: 'SearchView',
  components: {
    StarryBackground,
    Background,
    Guide,
  },
  data() {
    return {
      query: '',
      queryType: '0', // 默认选择关键字
      displayText: '',
      response: {
        result: []
      }, // 确保response默认是一个包含result数组的对象
      selectedFile: null,
      novelTitle: '', // 新增的小说标题字段
      userId: '', // 新增的用户ID字段
      type: 0,
      searchOptions: [
        { label: '关键字', value: '0' },
        { label: '小说id', value: '1' },
        { label: '作者id', value: '2' },
        { label: '作者名', value: '3' }
      ]
    };
  },
  methods: {
    fetchWithTimeout(url, options, timeout = 10000) {
      return Promise.race([
        fetch(url, options),
        new Promise((_, reject) =>
          setTimeout(() => reject(new Error('请求超时')), timeout)
        )
      ]);
    },
    async download(nid, ntitle) {
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
              novel_id: String(nid)
            })
          }
        );
        if (response.status === 200) {
          const blob = await response.blob();
          const downloadUrl = window.URL.createObjectURL(blob);
          const link = document.createElement('a');
          link.href = downloadUrl;
          link.download = `${ntitle}.txt`; // 注意这里需要加上反引号 ` 符号
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
    },
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
      if (this.selectedFile) {
        this.novelTitle = this.selectedFile.name;
        // this.userId = localStorage.getItem('token') || '';
      }
    },
    // 上传文件到服务器
    async uploadFile() {
      if (!this.selectedFile) {
        console.error('没有选择文件');
        return;
      }

      const formData = new FormData();
      formData.append('file', this.selectedFile);
      formData.append('novel_title', this.novelTitle);
      formData.append('user_id', 1);

      try {
        const response = await axios.post('http://121.36.55.149/apis/uploadfile', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        console.log('文件上传成功', response.data);
        alert('文件上传成功');
        // 这里可以添加上传成功后的逻辑
      } catch (error) {
        console.error('文件上传失败', error);
        alert('文件上传失败');
      }
    }
  },
};
</script>


<style>
input.rounded-input,
select.rounded-select,
button.rounded-button {
  padding: 10px;
  margin-right: 10px;
  border-radius: 10px;
  /* 设置圆角 */
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
  font-size: 1.5em;
  /* 调整字体大小 */
  margin-bottom: 20px;
  /* 调整下边距 */
  color: #007bff;
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

.file-info {
  margin-top: 10px;
  background-color: rgba(255, 255, 255, 0.8);
  padding: 10px;
  border-radius: 5px;
  font-size: 20px;
  color: #333;
  width: 300px;
  /* 设置较小的宽度 */
  margin: 0 auto;
  /* 使元素水平居中 */
}
</style>
