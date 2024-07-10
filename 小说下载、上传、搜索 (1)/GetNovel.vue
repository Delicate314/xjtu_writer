<template>
  <div>
    <input v-model="novelId" placeholder="Enter novel ID" />
    <button @click="fetchFileContent">Fetch File Content</button>
    <div v-if="fileContent">
      <pre>{{ fileContent }}</pre>
      <div class="pagination">
        <button @click="previousPage" :disabled="page === 1">Previous</button>
        <span>Page {{ page }} of {{ totalPages }}</span>
        <button @click="nextPage" :disabled="page >= totalPages">Next</button>
      </div>
    </div>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      novelId: '',
      fileContent: '',
      error: null,
      page: 1,
      pageSize: 10,
      totalPages: 1
    };
  },
  methods: {
    async fetchFileContent() {
      this.error = null;
      this.fileContent = '';

      try {
        const response = await axios.get('http://127.0.0.1:8000/apis/getNovel', {
          params: {
            novel_id: this.novelId,
            page: this.page,
            page_size: this.pageSize
          },
          responseType: 'json' // 指定响应类型为 JSON
        });

        this.fileContent = response.data.content;
        this.totalPages = response.data.total_pages;
      } catch (error) {
        this.error = error.response ? error.response.data.detail : 'An error occurred';
        console.error('Error fetching file content:', error);
      }
    },
    nextPage() {
      if (this.page < this.totalPages) {
        this.page += 1;
        this.fetchFileContent();
      }
    },
    previousPage() {
      if (this.page > 1) {
        this.page -= 1;
        this.fetchFileContent();
      }
    }
  }
};
</script>

<style scoped>
input {
  padding: 5px;
  margin-right: 10px;
}
button {
  padding: 5px 10px;
}
pre {
  background-color: #f4f4f4;
  padding: 10px;
  border: 1px solid #ddd;
}
.error {
  color: red;
}
.pagination {
  margin-top: 10px;
}
.pagination button {
  margin: 0 5px;
}
</style>
