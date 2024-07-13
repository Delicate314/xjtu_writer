<template>
  <div>
    <my-dialog :visible.sync="dialogVisible" :detailData="selectedDetail"></my-dialog>
    <el-table
      :data="tableData"
      style="width: 100%"
      max-height="640px"
      :default-sort = "{prop: 'user_id', order: 'ascending'}"
      @sort-change="handleSortChange">
      <el-table-column fixed sortable prop="user_id" label="用户id" width="200"></el-table-column>
      <el-table-column sortable prop="user_name" label="用户名" width="200"></el-table-column>
      <el-table-column prop="UpdatedAt" label="最近更新时间" width="190"></el-table-column>
      <el-table-column fixed="right" label="操作" width="280">
        <template slot-scope="scope">
          <el-popconfirm
            popper-class="my-popconfirm"
            confirm-button-text="确定"
            cancel-button-text="取消"
            icon="el-icon-delete"
            icon-color="red"
            title="此操作无法撤销，确定删除该用户？"
            @confirm="deleteRow(scope.$index, tableData)">
            <el-button slot="reference" type="danger" size="small" style="max-width: 80px; margin-right: 10px;">删除用户</el-button>
          </el-popconfirm>
          <el-button style="max-width: 80px; margin-right: 10px;" type="primary" size="small"
            @click.native.prevent="detailRow(scope.$index, tableData)">
            详细信息
          </el-button>
          <el-popconfirm
            popper-class="my-popconfirm"
            confirm-button-text="确定"
            cancel-button-text="取消"
            icon="el-icon-info"
            icon-color="green"
            title="是否重置该用户的密码？"
            @confirm="resetPassword(scope.$index, tableData)">
            <el-button style="max-width: 80px;" slot="reference" type="success" size="small">重置密码</el-button>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="currentPage"
      :page-sizes="[10, 15, 20, 30]" 
      :page-size="pageSize"
      layout="total, sizes, prev, pager, next" 
      :total=row_count>
    </el-pagination>
  </div>
</template>

<script>
import MyDialog from './UserDetail.vue';
import { Message } from 'element-ui';

export default {
  name: "SearchResults",
  components: {
    MyDialog
  },
  props: {
    query: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      selectedDetail: {},
      dialogVisible: false,
      defaultSort: { prop: 'user_id', order: 'ascending' },
      tableData: [],
      currentPage: 1,
      pageSize: 10,
      row_count: 0,
      search_t: '',
      // url_api:'127.0.0.1:8000',
      url_api:'121.36.55.149/apis',
    };
  },
  watch: {
    query: {
      immediate: true,
      handler(newQuery) {
        this.currentPage = 1;
        this.fetchUsers(newQuery);
        this.search_t = newQuery;
      }
    }
  },
  computed: {
    paginatedData() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = this.currentPage * this.pageSize;
      return this.tableData.slice(start, end);
    }
  },
  methods: {
    async deleteRow(index, tableData) {
      const uid = tableData[index].user_id;
      const uname = tableData[index].user_name;
      await this.deleteuser({ uid, uname });
      console.log(`删除了第 ${index} 行数据`);
      await this.fetchUsers(this.search_t);
    },
    detailRow(index, tableData) {
      this.dialogVisible = true;
      this.selectedDetail = { 'user_id': tableData[index].user_id, 'user_name': tableData[index].user_name };
      console.log(`查看第 ${index} 行的详细信息`);
    },
    resetPassword(index, tableData) {
      const uid = tableData[index].user_id;
      const uname = tableData[index].user_name;
      this.resetpwd({ uid, uname });
      console.log(`重置了第 ${index} 行用户密码`);
    },
    handleSizeChange(val) {
      this.pageSize = val;
      this.currentPage = 1;
      this.fetchUsers(this.search_t);
    },
    handleCurrentChange(val) {
      this.currentPage = val;
      this.fetchUsers(this.search_t);
    },
    async handleSortChange({ prop, order }) {
      this.defaultSort.prop = prop;
      this.defaultSort.order = order;
      this.fetchUsers(this.search_t);
    },
    async fetchUsers(search_target) {
      const { prop, order } = this.defaultSort;
      const offset = (this.currentPage - 1) * this.pageSize;
      const row_count = this.pageSize;

      try {
        let url = `http://${this.url_api}/admin/getusers?offset=${offset}&row_count=${row_count}&order_by=${prop}&order_way=${order}`;

        if (search_target && search_target.trim() !== '') {
          url += `&search_target=${encodeURIComponent(search_target)}`;
        }

        const response = await fetch(url);
        const data = await response.json();

        if (data.users) {
          this.tableData = data.users;
        }
        if (data.count) {
          this.row_count = data.count[0];
        }
      } catch (error) {
        console.error('获取用户信息失败:', error);
        Message.error({
          message: `获取用户信息失败: ${error.detail}`,
          duration: 3000
        });
      }
    },
    async deleteuser({ uid, uname }) {
      try {
        const response = await this.$axios.delete(`http://${this.url_api}/admin/deleteuser?user_id=${uid}&user_name=${uname}`);
        console.log('删除成功:', response.data.message);
        Message.success({
          message:'删除用户成功',
          duration:3000
        })
      } 
      catch (error) {
        const error_info='';
        if (error.response) {
          if (error.response.status === 404) {
            error_info='用户未找到或不存在';
            console.error('用户未找到或不存在');
          } else if (error.response.status === 500) {
            error_info='服务器内部错误';
            console.error('服务器内部错误');
          } else {
            error_info=`未知错误:${error.response.detail}`
            console.error('未知错误:', error.response.detail);
          }
        } else {
          error_info=`请求失败:${ error.detail}`
          console.error('请求失败:', error.detail);
        }
        Message.error({
          message:`删除用户失败${error_info}`,
          duration:3000
        })
      }
    },
    async resetpwd({ uid, uname }) {
      try {
        const response = await this.$axios.post(`http://${this.url_api}/admin/resetpassword?user_name=${uname}&user_id=${uid}`);
        console.log('密码重置成功:', response.data.message);
        Message.success({
          message: `${response.data.message}`,
          duration: 3000
        });
      } 
      catch (error) {
        const error_info='';
        if (error.response) {
          if (error.response.status === 404) {
            error_info = '用户未找到或不存在';
            console.error('用户未找到或不存在');
          } else if (error.response.status === 500) {
            error_info ='服务器内部错误'
            console.error('服务器内部错误');
          } else {
            error_info =`未知错误: ${error.response.detail}`;
            console.error('未知错误:', error.response.detail);
          }
        } else {
          error_info =`请求失败: ${error.detail}`;
          console.error('请求失败:', error.detail);
        }
        Message.error({
          message:`重置密码失败${error_info}`,
          duration:3000
        })
      }
    }
  }
};
</script>

<style> 
.button {
  max-width: 80px;
  margin-left: 10px;
}

.my-popconfirm .el-popper {
  font-size: 14px;
}
.my-popconfirm .el-popconfirm__main {
  margin: 10px 0 13px;
}
.my-popconfirm .el-button--mini {
  height: 30px;
  width: 45px;
  padding: 2px 6px;
}

</style>
