<template>
  <div class="page-container">
    <el-container>
      <el-header class="el-header">
        <div class="search">
          <el-input v-model="input" placeholder="用户id或用户名搜索" class="search-input"></el-input>
          <el-button type="primary" icon="el-icon-search" class="search-button" @click="handleSearch">搜索</el-button>
        </div>
      </el-header>
      <el-main class="el-main">
        <div class="table-container">
          <SearchResults :query="searchQuery" />
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import SearchResults from "@/components/backend/SearchResults";

export default {
  name: "UserManage",
  components: {
    SearchResults,
  },
  data() {
    return {
      input: '',
      searchQuery: '',
    };
  },
  methods: {
    handleSearch() {
      this.searchQuery = this.input;
    },
  },
};
</script>

<style scoped>
.page-content {
  align-content: center;
}

.el-main {
  background-color: #E9EEF3;
  color: #333;
  text-align: center;
  line-height: 1;
  justify-content: center;
}

.el-header {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #dae0e8;
  color: #333;
  text-align: center;
  line-height: 1;
}

.search {
  min-width: 400px;
  display: flex;
  align-items: center;
}

.search-input .el-input__inner {
  height: 40px;
}

.search-button {
  max-width: 90px;
  height: 40px;
  margin-left: 10px;
}

.table-container {
  justify-content: center;
  /* 水平居中 */
  height: 100%;
  /* 确保容器高度占满可用空间 */
}
</style>
