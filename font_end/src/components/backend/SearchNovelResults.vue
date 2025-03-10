<template>
  <div class="table-wrapper" v-loading="loading">
    <my-dialog :visible.sync="dialogVisible" :novelId="selectedNovel" :novelName="selectedNovelName"></my-dialog>
    <comment-dialog :visible.sync="commentDialogVisible" :novelId="selectedNovel"
      :novelName="selectedNovelName"></comment-dialog>

    <el-table :data="tableData" style="width: 100%" max-height="650px"
      :default-sort="{ prop: 'novel_id', order: 'ascending' }" @sort-change="handleSortChange">
      <el-table-column fixed sortable prop="novel_id" label="小说id" width="150"></el-table-column>
      <el-table-column sortable prop="user_id" label="作者" width="150"></el-table-column>
      <el-table-column sortable prop="novel_title" label="小说标题" width="180"></el-table-column>
      <el-table-column prop="novel_description" label="小说简介" width="380"></el-table-column>
      <el-table-column sortable prop="novel_viewcount" label="浏览量" width="120"></el-table-column>
      <el-table-column fixed="right" label="操作" width="280">
        <template slot-scope="scope">
          <el-popconfirm popper-class="my-popconfirm" confirm-button-text="确定" cancel-button-text="取消"
            icon="el-icon-info" icon-color="red" title="此操作无法撤销，确定删除该小说？" @confirm="deleteRow(scope.$index, tableData)">
            <el-button slot="reference" type="danger" size="small"
              style="max-width: 80px; margin-right: 10px;">删除</el-button>
          </el-popconfirm>
          <el-button class="button" @click.native.prevent="detailRow(scope.$index, tableData)" type="primary"
            size="small">
            小说内容
          </el-button>
          <el-button class="button" @click.native.prevent="commentRow(scope.$index, tableData)" type="primary"
            size="small">
            查看评论
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="currentPage"
      :page-sizes="[10, 15, 20, 30]" :page-size="pageSize" layout="total, sizes, prev, pager, next" :total="row_count">
    </el-pagination>
  </div>
</template>


<script>
import MyDialog from '@/components/backend/NovelContent';
import { Message } from 'element-ui';
import CommentDialog from '@/components/backend/commentDialog.vue';

export default {
  name: "SearchNovelResults",
  props: {
    query: {
      type: String,
      required: true
    }
  },
  components: {
    MyDialog,
    CommentDialog,
  },
  data() {
    return {
      selectedNovel: 1,
      selectedNovelName: '',
      commentDialogVisible: false,
      dialogVisible: false,
      defaultSort: { prop: 'novel_id', order: 'ascending' },
      tableData: [],
      currentPage: 1,
      pageSize: 10,
      row_count: 0,
      test_mes: '',
      search_t: '',
      loading: false, // 添加 loading 状态
    };
  },
  computed: {
    paginatedData() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = this.currentPage * this.pageSize;
      return this.tableData.slice(start, end);
    }
  },
  watch: {
    query: {
      immediate: true,
      handler(newQuery) {
        this.currentPage = 1;
        this.fetchNovels(newQuery);
        this.search_t = newQuery;
      }
    }
  },
  methods: {
    async deleteRow(index, tableData) {
      // 删除操作逻辑
      const uid = tableData[index].novel_id;
      const uname = tableData[index].novel_title;
      await this.deletenovel({ uid, uname });
      console.log(`删除了第 ${index} 行数据`);
      await this.fetchNovels(this.search_t);
    },
    detailRow(index, tableData) {
      // 详细信息操作逻辑
      this.dialogVisible = true;
      this.selectedNovel = tableData[index].novel_id;
      this.selectedNovelName = tableData[index].novel_title;
      console.log(`查看第 ${index} 行的详细信息`);
    },
    commentRow(index, tableData) {
      this.selectedNovel = tableData[index].novel_id;
      this.commentDialogVisible = true;
      this.selectedNovelName = tableData[index].novel_title;
    },
    handleSizeChange(val) {
      this.pageSize = val;
      this.currentPage = 1;
      this.fetchNovels(this.search_t);
    },
    handleCurrentChange(val) {
      this.currentPage = val;
      this.fetchNovels(this.search_t);
    },
    async handleSortChange({ prop, order }) {
      this.defaultSort.prop = prop;
      this.defaultSort.order = order;
      this.loading = true; // 设置 loading 为 true
      await this.fetchNovels(this.search_t);
      this.loading = false; // 设置 loading 为 false
    },
    async fetchNovels(search_target) {
      this.loading = true; // 设置 loading 为 true
      const { prop, order } = this.defaultSort;
      const offset = (this.currentPage - 1) * this.pageSize;
      const row_count = this.pageSize;

      try {
        let url = `http://121.36.55.149/apis/admin/getNovel?offset=${offset}&row_count=${row_count}&order_by=${prop}&order_way=${order}`;

        if (search_target && search_target.trim() !== '') {
          url += `&search_target=${encodeURIComponent(search_target)}`;
        }

        const response = await fetch(url);
        const reponse_data = await response.json();

        if (response.status === 404) {
          throw new Error('数据库内没有小说');
        }

        if (reponse_data.data) {
          this.tableData = reponse_data.data;
        } else {
          this.tableData = [];
        }

        if (reponse_data.count) {
          this.row_count = reponse_data.count;
        } else {
          this.row_count = 0;
        }
      } catch (error) {
        this.tableData = [];
        this.row_count = 0;
        console.error('获取小说信息失败:', error);
        Message.error({
          message: `获取小说信息失败: ${error.message || error.detail}`,
          duration: 3000
        });
      }
      this.loading = false; // 设置 loading 为 false
    },
    async deletenovel({ uid, uname }) {
      try {
        const response = await this.$axios.delete(`http://121.36.55.149/apis/admin/deletenovel?novel_id=${uid}&novel_title=${uname}`);
        console.log('删除成功:', response.message);
        Message.success({
          message: '删除小说成功',
          duration: 3000
        });
      } catch (error) {
        let error_info = '';
        if (error.response) {
          // 根据状态码处理错误
          if (error.response.status === 404) {
            error_info = '小说未找到或不存在';
            console.error('小说未找到或不存在');
          } else if (error.response.status === 500) {
            error_info = '服务器内部错误';
            console.error('服务器内部错误');
          } else {
            error_info = `未知错误: ${error.response.detail}`;
            console.error('未知错误:', error.response.detail);
          }
        } else {
          error_info = `请求失败: ${error.detail}`;
          console.error('请求失败:', error.detail);
        }
        Message.error({
          message: `删除用户失败：${error_info}`,
          duration: 3000
        });
      }
    },
  }
};
</script>

<style scoped>
.table-wrapper {
  width: 100%;
}

.button {
  max-width: 80px;
  margin-left: 10px;
}
</style>
