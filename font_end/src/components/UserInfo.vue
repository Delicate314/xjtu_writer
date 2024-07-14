<template>
    <div class="user-info">
      <h2>用户信息</h2>
      <p><strong>用户名：</strong>{{ userInfo.user_name }}</p>
      <p><strong>密码：</strong>{{ userInfo.user_password }}</p>
  
      <h2>用户的所有小说</h2>
      <ul>
        <li v-for="novel in novels" :key="novel.novel_id">
          <h3>{{ novel.novel_title }}</h3>
          <p>{{ novel.novel_description }}</p>
          <p><strong>更新时间：</strong>{{ novel.UpdatedAt }}</p>
          <p><strong>浏览次数：</strong>{{ novel.novel_viewcount }}</p>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        userInfo: {},
        novels: [],
      };
    },
    created() {
      this.fetchUserInfo();
    },
    methods: {
      async fetchUserInfo() {
        try {
          const response = await this.$axios.post('/apis/user/ownInfo');
          this.userInfo = response.data.user_info;
          this.novels = response.data.novel;
        } catch (error) {
          console.error('An error occurred while fetching user information:', error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .user-profile {
    margin: 20px;
  }
  
  .user-profile h2 {
    margin-top: 20px;
  }
  
  .user-profile p {
    margin: 5px 0;
  }
  
  .user-profile ul {
    list-style-type: none;
    padding: 0;
  }
  
  .user-profile li {
    border: 1px solid #ccc;
    padding: 10px;
    margin: 10px 0;
  }
  </style>
  