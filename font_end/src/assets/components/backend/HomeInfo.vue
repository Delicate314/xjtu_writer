<template>
  <div>
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>个人信息</span>
      </div>
      <div class="text item">
        {{ item[0] + ":" + info[0] }}
      </div>
      <div class="text item">
        {{ item[1] + ":" + info[1] }}
      </div>
      <div class="text item password-row">
        <span>{{ item[2] + ":" }}</span>
        <el-button class="no-border-btn" type="text" @click="dialogFormVisible = true">修改密码</el-button>
      </div>
      <el-dialog title="修改密码" :visible.sync="dialogFormVisible">
        <el-form :model="form">
          <el-form-item label="旧密码" :label-width="formLabelWidth">
            <el-input v-model="form.oldPassword" show-password placeholder="请输入旧密码"></el-input>
          </el-form-item>
          <el-form-item label="请输入新密码" :label-width="formLabelWidth">
            <el-input v-model="form.newPassword" show-password placeholder="请输入新密码"></el-input>
          </el-form-item>
          <el-form-item label="确认新密码" :label-width="formLabelWidth">
            <el-input v-model="form.confirmPassword" show-password placeholder="确认新密码"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogFormVisible = false">取 消</el-button>
          <el-button type="primary" @click="handleConfirm">确 定</el-button>
        </div>
      </el-dialog>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'HomeInfo',
  data() {
    return {
      item: ['用户名', '权限', '密码'],
      info: ['Admin', '管理员'],
      dialogFormVisible: false,
      form: {
        oldPassword: '',
        newPassword: '',
        confirmPassword: ''
      },
      formLabelWidth: '120px',
      message: ''
    };
  },
  methods: {
    async handleConfirm() {
      this.dialogFormVisible = false;
      console.log('确定按钮被点击');
      
      // 检查新密码和确认新密码是否一致
      if (this.form.newPassword !== this.form.confirmPassword) {
        this.message = '新密码和确认密码不一致';
        this.showError(this.message);
        return;
      }

      // 请求更改密码接口
      try {
        const response = await axios.post(`http://121.36.55.149/apis/admin/changepwd?user_password=${this.form.oldPassword}&user_newpassword=${this.form.newPassword}`);
        this.message = response.data.message;
        this.showSuccess(this.message);
      } catch (error) {
        if (error.response) {
          this.message = error.response.data.detail;
        } else {
          this.message = '密码修改失败';
        }
        this.showError(this.message);
      }
    },
    showError(message) {
      this.$alert(message, '错误', {
        confirmButtonText: '确定',
        type: 'error',
        callback: action => {
          this.$message({
            type: 'error',
            message: `action: ${ action }`
          });
        }
      });
    },
    showSuccess(message) {
      this.$message({
        type: 'success',
        message: message
      });
    }
  }
};
</script>

<style scoped>
.text {
  font-size: 14px;
}

.item {
  margin-bottom: 18px;
}

.password-row {
  display: flex;
  align-items: center;
}

.password-row span {
  margin-right: 10px;
}

.no-border-btn {
  max-width: 0px;
  border: none;
  padding: 0;
  color: #409EFF;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}
.clearfix:after {
  clear: both;
}

.box-card {
  width: 480px;
}
.dialog-footer{
  display:flex;
  max-width: 100px;
}
</style>
