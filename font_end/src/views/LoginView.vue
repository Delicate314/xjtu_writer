<template>
  <div>
    <h2>用户登录</h2>
    <input type="text" placeholder="用户名" v-model="username">
    <input type="password" placeholder="密码" v-model="password">
    <button @click="login">Login</button>
    <button @click="register">Register</button>
  </div>
</template>

<script>
export default {
  name: 'LoginView',
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    login() {
      console.log('Logging in', this.username);
      // Add your login logic here
      this.$router.push('/Home')
      
    },
    register() {
      //console.log('Logging in', this.username);
      // Add your login logic here
      this.$router.push('/register')
      
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
