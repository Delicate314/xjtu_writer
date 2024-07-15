<template>
  <div>
    <el-container>
      <el-aside width="220px">
        <div class="custom-header">
          <img src="@/assets/backend_logo/mylogo.png" alt="图片描述" class="custom-img">
          <h5 class="custom-title">XJTU小说家</h5>
        </div>
        <el-row class="tac">
          <el-col :span="24">
            <el-menu default-active="2" class="el-menu-vertical-demo" @select="handleSelect" background-color="#2c3f5b"
              text-color="#fff" active-text-color="#2586fe" :style="{ width: '100%' }">
              <el-menu-item index="2">
                <i class="el-icon-location"></i>
                <span slot="title">首页</span>
              </el-menu-item>
              <el-menu-item index="3">
                <i class="el-icon-user-solid"></i>
                <span slot="title">用户管理</span>
              </el-menu-item>
              <el-menu-item index="4">
                <i class="el-icon-menu"></i>
                <span slot="title">小说管理</span>
              </el-menu-item>
            </el-menu>
          </el-col>
        </el-row>
      </el-aside>

      <el-container>
        <el-header>
          <el-row :gutter="20">
            <el-col :span="6">
              <div class="grid-content bg-purple">
                <i class="el-icon-wallet"></i>
                {{ currentHeader }}
              </div>
            </el-col>
            <el-col :span="4" :offset="14">
              <div class="right-content bg-purple">
                <div class="user-content">
                  欢迎你 管理员
                  <img src="@/assets/backend_logo/user.gif" alt="" class="user-img">
                </div>
              </div>
            </el-col>
          </el-row>
        </el-header>


        <el-main>
          <component :is="currentComponent"></component>
        </el-main>

      </el-container>
    </el-container>
  </div>
</template>

<script>
import Novel from "@/components/backend/novel";
import User from "@/components/backend/UserManage";
import Home from '@/components/backend/AdminHomePage';
import axios from 'axios';

export default {
  components: {
    Novel,
    User,
    Home
  },
  data() {
    return {
      breadcrumb: '首页',
      pageIndex: 2
    }
  },
  methods: {
    handleSelect(key) {
      this.pageIndex = key;
    },
    async checkAdmin() {
      try {
        const response = await axios.post("http://121.36.55.149:80/apis/user/is_admin");
        console.log(response);
        if (response.data.user_isadmin === '0') {
          this.$router.push('/login');
        }
      } catch (error) {
        console.error("Error checking admin status:", error);
        this.$router.push('/login');
      }
    }
  },
  computed: {
    currentComponent() {
      switch (this.pageIndex) {
        case '2':
          return Home;
        case '3':
          return User;
        case '4':
          return Novel;
        default:
          return Home;
      }
    },
    currentHeader() {
      switch (this.pageIndex) {
        case '2':
          return "首页";
        case '3':
          return "用户管理";
        case '4':
          return "小说管理";
        default:
          return "首页";
      }
    }
  },
  mounted() {
    this.checkAdmin();
  },
}
</script>



<style>
.user-content {
  display: flex;
  text-align: right;
  align-items: center;
  /* 使文字和图片的中点水平对齐 */
}

.user-img {
  margin-left: 20px;
  /* 调整图片和文字之间的距离 */
  border-radius: 50%;
  /* 使用圆角 */
  width: 40px;
  /* 固定宽度，保证圆角效果 */
  height: 40px;
  /* 固定高度，保证圆角效果 */
}


.el-col {
  border-radius: 4px;
}

.bg-purple {
  background: #ffffff;
}

.grid-content {
  border-radius: 4px;
  text-indent: 10px;
  min-height: 36px;
  text-align: left;
  color: #909399;
}

.right-content {
  border-radius: 4px;
  min-height: 36px;
  text-align: right;
}

.el-header,
.el-footer {
  background-color: #ffffff;
  color: #333;
  text-align: center;
  line-height: 60px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)
}

.el-aside {
  background-color: #2c3f5b;
  color: #2586fe;
  text-align: center;
  height: 100vh;
  /* 高度填满视口 */
}

.el-main {
  background-color: #edeee930;
  color: #333;
  text-align: start;
  height: 85vh;
  /* 高度填满视口 */
  line-height: 85vh;
  /* 使文本垂直居中 */
}

body>.el-container {
  margin-bottom: 40px;
}

.custom-header {
  text-align: center;
  display: flex;
  padding: 10px;
  align-items: center;
  background-color: #2c3f5b;
}

.el-menu-vertical-demo {
  text-align: left;
  /* 菜单项左对齐 */
}

.custom-img {
  width: 40px;
  /* 图片宽度与文字大小一致 */
  height: 40px;
  /* 图片高度与文字大小一致 */
  margin-right: 20px;
  /* 图片右侧留出一些空间 */
}

.custom-title {
  margin: 0;
  /* 去除标题的默认外边距 */
  padding: 0;
  font-size: 22px;
  color: #E9EEF3;
}
</style>