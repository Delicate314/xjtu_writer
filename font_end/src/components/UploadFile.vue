<template>
  <div class="upload-component">
    <h2 class="link1">上传小说到社区</h2>
    <input type="file" @change="handleFileUpload" />
    <div v-if="selectedFile" class="file-info">
      <p>已选择文件：{{ selectedFile.name }}</p>
    </div>
    <button @click="uploadFile" class="upload rounded-button">上传文件</button>
  </div>
</template>

<script>
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

.rounded-input,
.rounded-button {
  margin-right: 10px;
  padding: 10px;
  border-radius: 5px;
}

.rounded-button {
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}

.rounded-button:hover {
  background-color: #0056b3;
}

.file-info {
  margin-top: 10px;
}
</style>