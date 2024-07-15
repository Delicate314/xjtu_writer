<template>
  <div class="rank-container">
    <h2 class="title">小说排名</h2>
    <table>
      <thead>
        <tr>
          <th class="rank-top">排名</th>
          <th>书名</th>
          <th>作者</th>
          <th class="rank-bottom">热度</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in novels" :key="index" class="rank-item">
          <td>{{ index + 1 + (currentPage - 1) * itemsPerPage }}</td>
          <td>
            <router-link :to="`/Novel?id=${item.novel_id}`" class="item-link">
              {{ item.novel_title }}
            </router-link>
          </td>
          <td>{{ item.user_name }}</td>
          <td>{{ item.novel_viewcount }}</td>
        </tr>
      </tbody>
    </table>
    <div class="pagination">
      <button @click="prevPage" :disabled="currentPage === 1">上一页</button>
      <span>Page {{ currentPage }}</span>
      <button @click="nextPage">下一页</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RankTable',
  data() {
    return {
      novels: [],
      currentPage: 1,
      itemsPerPage: 10,
    };
  },
  mounted() {
    this.getRank();
  },
  methods: {
    async getRank() {
      console.log('Fetching novel rank...');
      try {
        const params = {
          index: this.currentPage,
          itemsPerPage: this.itemsPerPage
        };
        const response = await this.$axios.post('http://121.36.55.149:80/apis/rank', params);
        this.novels = response.data;
        console.log('Novels:', this.novels);
      } catch (error) {
        console.error('Error fetching novel rank:', error);
      }
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
        this.getRank();
      }
    },
    nextPage() {
      this.currentPage++;
      this.getRank();
    }
  }
};
</script>

<style scoped>
.rank-container {
  width: 600px;
  height: 600px;
  margin: 30px auto;
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.title {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
  font-family: 'Courier New', Courier, monospace;
  font-size: 24px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 10px;
  text-align: center;
}

th {
  background-color: #f4f4f4;
}

.rank-top {
  border-top-left-radius: 8px;
  border-bottom-left-radius: 8px;
}

.rank-bottom {
  border-top-right-radius: 8px;
  border-bottom-right-radius: 8px;
}

.rank-item {
  background-color: #fafafa;
  border-bottom: 1px solid #eaeaea;
}

.item-link {
  color: #3498db;
  text-decoration: none;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.pagination button {
  background-color: #3498db;
  color: #fff;
  border: none;
  padding: 10px;
  margin: 0 5px;
  border-radius: 4px;
  cursor: pointer;
}

.pagination button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.pagination span {
  padding: 10px;
}
</style>
