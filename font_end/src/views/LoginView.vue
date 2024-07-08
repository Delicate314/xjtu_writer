<template>
  <div>
    <h2>用户登录</h2>
    <input type="text" placeholder="用户名" v-model="username">
    <input type="password" placeholder="密码" v-model="password">
    <button @click="login">登录</button>
    <button @click="register">注册</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'LoginView',
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    async login() {
      console.log('登录用户名：', this.username);
      try {
        const response = await axios.post('http://localhost:8000/apis/login/', { // 后端服务器运行地址
          user_name: this.username,
          user_pwd: this.password
        });
        if (response.data.success === true) {
          console.log('登录成功');
          this.$router.push('/Home');
          return true;
        } else {
          console.error('登录失败:', response.data.detail);
          return false;
        }
      } catch (error) {
        console.error('登录过程中出现错误:', error);
        return false;
      }
    },
    register() {
      this.$router.push('/register');
    },
  },
};
</script>

<style>
input {
  display: block;
  width: 200px;
  padding: 10px;
  margin: 10px auto;
}

button {
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>
