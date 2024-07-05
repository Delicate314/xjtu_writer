<template>
  <div class="register-container">
    <h2>Register</h2>
    <input type="text" placeholder="Username" v-model="username">
    <input type="email" placeholder="Email" v-model="email">
    <input type="password" placeholder="Password" v-model="password">
    <button @click="register">Register</button>
  </div>
</template>

<script>
export default {
  name: 'Register',
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
    },
  },
};
</script>

<style>
.register-container {
  max-width: 300px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
  background-color: #fff;
}
input {
  display: block;
  width: 100%;
  padding: 10px;
  margin: 10px 0;
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
