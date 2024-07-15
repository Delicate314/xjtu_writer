<template>
  <div class="user-profile">
    <div class="container">
      <div class="user-panel">
        <button @click="toggleUserInfoVisibility" class="toggle-button">我的信息</button>
        <div class="user-info" :class="{ 'info-visible': userInfoVisible, 'info-hidden': !userInfoVisible }">
          <div class="info">
            <p><strong>用户名：</strong>{{ user_name }}</p>
            <p><strong>密码：</strong><span v-if="showPassword">{{ user_password }}</span><span v-else>******</span></p>
            <button @click="togglePasswordVisibility" class="button">{{ showPassword ? '隐藏密码' : '显示密码' }}</button>
          </div>
        </div>
      </div>
      <div class="novel">
        <UserNovel />
      </div>
    </div>
  </div>
</template>

<script>
import UserNovel from '@/components/UserNovel.vue';
export default {
  components: {
    UserNovel,
  },
  data() {
    return {
      user_id: null,
      user_name: null,
      user_password: null,
      userInfoVisible: true,
      showPassword: false
    };
  },
  mounted() {
    this.fetchUserInfo();
  },
  methods: {
    async fetchUserInfo() {
      try {
        const { data } = await this.$axios.post("http://121.36.55.149:80/apis/user/ownInfo");
        this.user_id = data.user_info.user_id;
        this.user_name = data.user_info.user_name;
        this.user_password = data.user_info.user_password;
      } catch (error) {
        console.error('An error occurred while fetching user information:', error);
      }
    },
    togglePasswordVisibility() {
      this.showPassword = !this.showPassword;
    },
    toggleUserInfoVisibility() {
      this.userInfoVisible = !this.userInfoVisible;
    }
  },
};
</script>

<style scoped>
.toggle-button {
  height: 100%;
  /* 调整按钮高度 */
  width: 25px;
  /* 调整按钮宽度 */
  margin: 10px;
  padding: 5px 5px;
  font-size: 14px;
  color: #fff;
  background-color: #007bff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.toggle-button:hover {
  opacity: 0.8;
}

.user-profile {
  margin-top: 20px;
  padding: 10px;
  background-color: #f5f5f5;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.container {
  height: 600px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-panel {
  height: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
}

.user-info {
  width: 200px;
  /* 初始宽度 */
  height: 100%;
  /* 占据全部高度 */
  overflow: hidden;
  /* 超出部分隐藏 */
  transition: width 0.3s ease;
  /* 宽度过渡效果 */
}

.info-visible {
  width: 150px;
  height: 100%;
  /* 展开后的宽度 */
}

.info-hidden {
  width: 0;
  height: 100%;
  /* 折叠后的宽度 */
}

.info {
  height: 100%;
  padding: 20px;
  border-radius: 10px;
  background-color: #ffffff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.info p {
  margin: 5px 0;
  color: #555;
}

.button {
  margin-top: 10px;
  padding: 5px 10px;
  font-size: 14px;
  color: #fff;
  background-color: #007bff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.button:hover {
  opacity: 0.8;
}

.novel {
  margin: 0px;
  width: 100%;
  align-self: flex-start;
  /* 也可以直接在子元素上设置 */
}
</style>
