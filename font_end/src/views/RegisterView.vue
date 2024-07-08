<template>
  <div>
    <h2>用户注册</h2>
    <input type="text" placeholder="用户名" v-model="username">
    <input type="email" placeholder="邮箱" v-model="email">
    <input type="password" placeholder="密码" v-model="password">
    <button @click="register">Register</button>
  </div>
</template>

<script>
export default {
  name: 'RegisterView',
  data() {
    return {
      username: '',
      email: '',
      password: '',
    };
  },
  methods: {
    register() {
      console.log('Registering', this.username);
      // Add your register logic here
      this.$router.push('/')
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
