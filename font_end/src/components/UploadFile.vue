<template>
  <div class="upload-component">
    <h2 class="link1">上传小说到社区</h2>
    <el-upload class="upload-demo" drag action="http://121.36.55.149/apis/uploadfile" :on-change="handleFileChange"
      :before-upload="beforeUpload" :data="uploadData" :show-file-list="false">
      <i class="el-icon-upload"></i>
      <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
    </el-upload>
    <el-dialog :visible.sync="dialogVisible" title="请输入小说标题" class="input_title">
      <el-input v-model="novelTitle" placeholder="请输入小说标题" />
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="confirmUpload" v-loading="loading">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { MessageBox } from 'element-ui';
import axios from 'axios';
export default {
  name: 'UploadComponent',
  data() {
    return {
      loading: false,
      selectedFile: null,
      novelTitle: '',
      userId: '', // 可以根据需要进行处理，如使用 localStorage.getItem('token') 获取用户 ID
      dialogVisible: false,
      uploadData: {
        novel_title: '',
        user_id: 1, // 暂时写死用户 ID，可以根据实际情况处理
      },
    };
  },
  methods: {
    handleFileChange(file) {
      this.selectedFile = file.raw;
      if (this.selectedFile) {
        this.novelTitle = this.selectedFile.name;
      }
    },
    beforeUpload(file) {
      this.selectedFile = file;
      this.dialogVisible = true;
      return false; // 阻止自动上传
    },
    async confirmUpload() {
      if (!this.novelTitle) {
        console.error('小说标题为空');
        MessageBox.alert('小说标题不能为空', '错误', {
          confirmButtonText: '确定',
          type: 'error',
        });
        return;
      }
      const formData = new FormData();
      formData.append('file', this.selectedFile);
      formData.append('novel_title', this.novelTitle);
      this.loading = true;
      try {
        const response = await axios.post('http://121.36.55.149/apis/uploadfile', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        console.log('文件上传成功', response.data);
        this.$message.success('文件上传成功');
        // 这里可以添加上传成功后的逻辑
        this.loading = false;
        this.dialogVisible = false; // 关闭对话框
      } catch (error) {
        console.error('文件上传失败', error);
        MessageBox.alert(`文件上传失败,仅支持.txt格式`, '错误', {
          confirmButtonText: '确定',
          type: 'error',
        });
        this.dialogVisible = false; // 关闭对话框
      }
    }
  }
};
</script>

<style scoped>
.upload-component {
  margin: 20px auto;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  width: 90%;
  max-width: 400px;
  /* Limit maximum width for larger screens */
  overflow: hidden;
  /* Ensure no overflow on smaller screens */
}

.upload-demo {
  border: 2px dashed #d9d9d9;
  border-radius: 6px;
  text-align: center;
  padding: 20px;
}

.el-upload__text em {
  color: #409eff;
}

h2.link1 {
  font-size: 1.5em;
  margin-bottom: 20px;
  color: #fff;
}

.file-info {
  margin-top: 10px;
  background-color: rgba(255, 255, 255, 0.8);
  padding: 10px;
  border-radius: 5px;
  font-size: 20px;
  color: #333;
  width: 300px;
  margin: 0 auto;
}

.input_title {
  margin: 0px auto;
  width: 80%;
}

@media (max-width: 768px) {
  .upload-component {
    width: 90%;
    /* Adjusted width for mobile responsiveness */
    max-width: none;
  }

  .el-upload__text {
    width: 100%;
    /* Full width for text in mobile */
  }

  .input_title {
    width: 80%;
  }
}
</style>
