<template>
  <div class="login-background">
    <StarryBackground />
    <div class="header-title">
      <h1 class="main-title">XJTU AI-Writer</h1>
    </div>
    <div class="login-container">
      <el-card class="login-card" shadow="hover">
        <div class="title-container">
          <h2 class="login-title">用户登录</h2>
        </div>
        <el-form :model="form" status-icon :rules="rules" ref="form">
          <el-form-item prop="username">
            <el-input v-model="form.username" placeholder="用户名" @keyup.enter.native="focusPasswordInput"></el-input>
          </el-form-item>
          <el-form-item prop="password">
            <el-input ref="password" type="password" v-model="form.password" placeholder="密码"
              @keyup.enter.native="login"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="login">登录</el-button>
          </el-form-item>
          <el-form-item>
            <el-button type="success" @click="register">注册</el-button>
          </el-form-item>
        </el-form>
        <div class="extra-options">
          <el-button type="text" @click="forgotPassword">忘记密码?</el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { MessageBox } from 'element-ui';
import StarryBackground from '@/components/StarryBackground.vue';

export default {
  name: 'LoginView',
  components: {
    StarryBackground,
  },

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
    focusPasswordInput() {
      this.$refs.password.focus();
    },
    async login() {
      this.$refs.form.validate(async (valid) => {
        if (valid) {
          try {
            const params = new URLSearchParams();
            params.append('username', this.form.username);
            params.append('password', this.form.password);

            const response = await axios.post('http://121.36.55.149/apis/login/', params);

            console.log("response: ", response.data);
            window.sessionStorage.setItem('token', response.data.access_token);
            window.sessionStorage.setItem('passport', this.$message.success)
            const token = `Bearer ${response.data.access_token}`;
            window.sessionStorage.setItem('token', token);
            if (response.data.is_admin == 1) {
              this.$message.success('进入管理员系统');
              this.$router.push('/Admin');
            } else if (response.data.success) {
              this.$message.success('登录成功');
              this.$router.push('/Home');
            } else {
              MessageBox.alert(`登录失败: ${response.data.detail}`, '错误', {
                confirmButtonText: '确定',
                type: 'error',
              });
            }
          } catch (error) {
            MessageBox.alert(`用户名或密码错误！`, '错误', {
              confirmButtonText: '确定',
              type: 'error',
            });
          }
        }
      });
    },
    register() {
      this.$router.push('/register');
    },
    forgotPassword() {
      this.$message.info('请联系管理员重置密码');
    },
  },
};
</script>

<style scoped>
.login-background {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  position: relative;
  overflow: hidden;
}

.login-background::before {
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

.header-title {
  position: absolute;
  top: 5%;
  width: 100%;
  text-align: center;
  z-index: 2;
}

.main-title {
  font-size: 48px;
  background: -webkit-linear-gradient(135deg, #3f87a6, #ebf8e1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: bold;
}

.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  z-index: 2;
}

.login-card {
  width: 400px;
  padding: 20px;
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

.login-title {
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

.el-divider {
  margin: 20px 0;
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

/* 移动端适配 */
@media (max-width: 768px) {
  .main-title {
    font-size: 36px;
  }

  .login-card {
    width: 90%;
    padding: 10px;
  }

  .login-title {
    font-size: 20px;
  }

  .el-button,
  .el-form-item input {
    font-size: 14px;
  }

  .el-form-item {
    margin-bottom: 15px;
  }

  .extra-options {
    justify-content: center;
  }
}
</style>
