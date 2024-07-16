<template>
  <div class="register-container">
    <StarryBackground />
    <div class="header-title">
      <h1 class="main-title">XJTU AI-Writer</h1>
    </div>
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
        <el-form-item prop="confirmPassword">
          <el-input type="password" v-model="form.confirmPassword" placeholder="确认密码"></el-input>
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
import StarryBackground from '@/components/StarryBackground.vue';

export default {
  name: 'RegisterView',
  components: {
    StarryBackground,
  },
  data() {
    return {
      form: {
        username: '',
        password: '',
        confirmPassword: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { validator: this.validatePassword, trigger: 'blur' },
        ],
        confirmPassword: [
          { required: true, message: '请再次输入密码', trigger: 'blur' },
          { validator: this.validateConfirmPassword, trigger: 'blur' },
        ],
      },
    };
  },
  methods: {
    validatePassword(rule, value, callback) {
      const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{6,20}$/;
      if (!value) {
        callback(new Error('请输入6到20位的大小写字母和数字组合的密码'));
      } else if (!passwordPattern.test(value)) {
        callback(new Error('密码必须是6到20位的大小写字母和数字组合'));
      } else {
        callback();
      }
    },
    validateConfirmPassword(rule, value, callback) {
      if (value !== this.form.password) {
        callback(new Error('两次输入的密码不一致'));
      } else {
        callback();
      }
    },
    async register() {
      this.$refs.form.validate(async (valid) => {
        if (valid) {
          try {
            const response = await axios.post('http://121.36.55.149:80/apis/register/', {
              user_name: this.form.username,
              user_pwd: this.form.password,
            });
            console.log(response);
            if (response.data.success) {
              this.$message.success('注册成功');
              this.$router.push('/');
            }
            else if (response.data.msg == '用户名重复！') {
              MessageBox.alert(`注册失败: 用户名重复！`, '错误', {
                confirmButtonText: '确定',
                type: 'error',
              })
            }
            else {
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
      this.$router.push('/');
    },
  },
};
</script>

<style scoped>
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

.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
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

/* 移动端适配 */
@media (max-width: 768px) {
  .register-card {
    width: 90%;
    padding: 10px;
  }

  .register-title {
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
