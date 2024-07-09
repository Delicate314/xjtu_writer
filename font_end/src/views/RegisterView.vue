<template>
  <div class="register-container">
    <el-card class="register-card" shadow="hover">
      <div class="title-container">
        <h2 class="register-title">用户注册</h2>
      </div>
      <el-form :model="form" status-icon :rules="rules" ref="form">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="用户名"></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input type="password" v-model="form.password" placeholder="密码"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="register">注册</el-button>
        </el-form-item>
      </el-form>
      <div class="extra-options">
        <el-button type="text" @click="goToLogin">已有账户？登录</el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios';
import { MessageBox } from 'element-ui';

export default {
  name: 'RegisterView',
  data() {
    return {
      form: {
        username: '',
        password: '',
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
        ],
      },
    };
  },
  methods: {
    async register() {
      this.$refs.form.validate(async (valid) => {
        if (valid) {
          try {
            const response = await axios.post('http://localhost:8000/register/', {
              user_name: this.form.username,
              user_pwd: this.form.password,
            });
            if (response.data.success) {
              this.$message.success('注册成功');
              this.$router.push('/login');
            } else {
              MessageBox.alert(`注册失败: ${response.data.detail}`, '错误', {
                confirmButtonText: '确定',
                type: 'error',
              });
            }
          } catch (error) {
            MessageBox.alert(`注册失败，请重试！`, '错误', {
              confirmButtonText: '确定',
              type: 'error',
            });
          }
        }
      });
    },
    goToLogin() {
      this.$router.push('/login');
    },
  },
};
</script>

<style>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #2c3e50, #3498db);
  position: relative;
  overflow: hidden;
}

.register-container::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle at center, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
  transform: rotate(45deg);
  z-index: 1;
}

.register-card {
  width: 400px;
  padding: 20px;
  position: relative;
  z-index: 2;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
}

.title-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 20px;
}

.register-title {
  font-size: 24px;
  color: #333;
  margin: 0;
}

.el-button {
  width: 100%;
  margin-bottom: 10px;
}

.el-form-item {
  margin-bottom: 20px;
}

.extra-options {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}

::placeholder {
  color: #ccc;
  font-style: italic;
}

.el-form-item input {
  background: rgba(255, 255, 255, 0.6);
  border-radius: 5px;
}

.el-form-item input:hover {
  background: rgba(255, 255, 255, 0.8);
}

.el-form-item input:focus {
  background: rgba(255, 255, 255, 1);
}
</style>
