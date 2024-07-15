<template>
  <div class="upload-component">
    <h2 class="link1">上传小说到社区</h2>
    <input type="file" @change="handleFileUpload" />
    <div v-if="selectedFile" class="file-info">
      <p>已选择文件：{{ selectedFile.name }}</p>
    </div>
    <button @click="uploadFile" class="rounded-button">上传文件</button>
  </div>
</template>

<script scoped>
import axios from 'axios';
import { MessageBox } from 'element-ui';

export default {
  name: 'UploadComponent',
  data() {
    return {
      selectedFile: null,
      novelTitle: '',
      userId: '', // 可以根据需要进行处理，如使用 localStorage.getItem('token') 获取用户 ID
    };
  },
  methods: {
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0];
      if (this.selectedFile) {
        this.novelTitle = this.selectedFile.name;
      }
    },
    async uploadFile() {
      if (!this.selectedFile) {
        console.error('没有选择文件');
        return;
      }

      const formData = new FormData();
      formData.append('file', this.selectedFile);
      formData.append('novel_title', this.novelTitle);
      formData.append('user_id', 1); // 暂时写死用户 ID，可以根据实际情况处理

      try {
        const response = await axios.post('http://121.36.55.149/apis/uploadfile', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        console.log('文件上传成功', response.data);
        this.$message.success('文件上传成功');
        // 这里可以添加上传成功后的逻辑
      } catch (error) {
        console.error('文件上传失败', error);
        MessageBox.alert(`文件上传失败`, '错误', {
          confirmButtonText: '确定',
          type: 'error',
        });
      }
    }
  }
};
</script>

<style>
.upload-component {
  margin: 20px;
  padding: 20px;
  background-color: rgba(255, 255, 255, 0.6);
  /* 半透明白色背景 */
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  /* 轻微阴影效果 */
}

button.rounded-button {
  padding: 13px 30px;
  background-color: #5f87b5;
  color: #fff;
  font-family: '微软雅黑';
  font-weight: bold;
  font-size: 16px;
  border: none;
  cursor: pointer;
  margin-right: 10px;
  border-radius: 10px;
}

button.rounded-button:hover {
  background-color: #0056b3;
}

.file-info {
  margin-top: 10px;
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

.file-load {
  padding: 13px 20px;
  margin-right: 10px;
  border-radius: 10px;
  border: 3px solid #112d4e;
  font-size: 15px;
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

.file-info {
  margin-top: 10px;
  background-color: rgba(255, 255, 255, 0.8);
  /* 设置背景颜色并添加透明度 */
  padding: 10px;
  /* 设置内边距 */
  border-radius: 5px;
  /* 设置圆角 */
  font-size: 20px;
  /* 设置字体大小 */
  color: #333;
  /* 设置字体颜色 */
  width: 300px;
  /* 设置较小的宽度 */
  margin: 0 auto;
  /* 使元素水平居中 */
}
</style>