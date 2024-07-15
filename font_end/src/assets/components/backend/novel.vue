<template>
  <div class="page-container">
    <el-container>
      <el-header class="el-header">
        <div class="search">
          <el-input v-model="input" placeholder="小说id或用户id或小说名搜索" class="search-input"></el-input>
          <el-button type="primary" icon="el-icon-search" class="search-button" @click="handleSearch">搜索</el-button>
        </div>
      </el-header>
      <el-main class="el-main">
        <div class="table-container">
          <SearchNovelResults :query="searchQuery" />
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import SearchNovelResults from "@/components/backend/SearchNovelResults"; 

export default {
  name: "UserManage",
  components: {
    SearchNovelResults,
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
.page-container {
  width: 100%;
  height: 80vh;
}

.el-main {
  background-color: #E9EEF3;
  color: #333;
  text-align: center;
  line-height: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  flex-grow: 1;
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
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
}
</style>
