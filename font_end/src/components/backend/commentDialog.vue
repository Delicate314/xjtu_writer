<template>
  <el-dialog :visible.sync="visible" width="70%" @close="handleClose">
    <span slot="title">《{{ novelName }}》 的评论</span>
    <el-table v-if="!loading && !error" :data="comments" style="width: 100%">
      <el-table-column prop="user_id" label="用户" width="150"></el-table-column>
      <el-table-column prop="updateAt" label="更新时间" width="200"></el-table-column>
      <el-table-column prop="comment_content" label="评论内容" width="400"></el-table-column>
      <el-table-column fixed="right" label="操作" width="280">
        <template slot-scope="scope">
          <el-popconfirm
            popper-class="my-popconfirm"
            confirm-button-text="确定"
            cancel-button-text="取消"
            icon="el-icon-info"
            icon-color="red"
            title="此操作无法撤销，确定删除该评论？"
            @confirm="deleteRow(scope.$index, comments)"
          >
            <el-button slot="reference" type="danger" size="small" style="max-width: 80px; margin-right: 10px;">删除评论</el-button>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>
    <div v-if="loading" class="loading-container">
      <el-spinner type="circle"></el-spinner>
      <span>加载中...</span>
    </div>
    <div v-if="error" class="error-container">
      <el-icon class="error-icon"><i class="el-icon-warning-outline"></i></el-icon>
      <span>获取评论失败，请重试</span>
    </div>
  </el-dialog>
</template>

<script>
import axios from 'axios';
import { Message } from 'element-ui';

export default {
  name: 'CommentDialog',
  props: {
    visible: {
      type: Boolean,
      required: true,
    },
    novelId: {
      type: Number,
      required: true,
    },
    novelName: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      comments: [],
      loading: false,
      error: false,
    };
  },
  watch: {
    visible(newVal) {
      if (newVal) {
        this.fetchComments();
      }
    }
  },
  methods: {
    async deleteRow(index, tableData) {
      // 删除操作逻辑
      const uid = tableData[index].comment_id;
      try {
        await this.deletecomment({ index, uid });
        Message.success({
          message: '删除评论成功',
          duration: 3000
        });
        this.fetchComments(); // 删除成功后重新获取评论数据
        console.log(`删除了第 ${index} 行数据`);
      } catch (error) {
        console.error('删除失败:', error);
      }
    },
    async fetchComments() {
      this.loading = true;
      this.error = false;
      try {
        const response = await axios.get(`http://121.36.55.149/apis/admin/getnovelcomment?novel_id=${this.novelId}`);
        this.comments = response.data.data;
      } catch (error) {
        console.error('获取评论失败:', error);
        this.error = true;
      } finally {
        this.loading = false;
      }
    },
    handleClose() {
      this.$emit('update:visible', false);
    },
    async deletecomment({ index, uid }) {
      try {
        const response = await axios.delete(`http://121.36.55.149/apis/admin/deletecomment?comment_id=${uid}`);
        console.log('删除成功:', response.message);
      } catch (error) {
        if (error.response) {
          let error_info = '';
          // 根据状态码处理错误
          if (error.response.status === 404) {
            error_info = '评论未找到或不存在';
            console.error('评论未找到或不存在');
          } else if (error.response.status === 500) {
            error_info = '服务器内部错误';
            console.error('服务器内部错误');
          } else {
            error_info = `未知错误:${error.response.detail}`;
            console.error('未知错误:', error.response.detail);
          }
          Message.error({
            message: `删除评论失败：${error_info}`,
            duration: 3000
          });
        } else {
          const error_info = `请求失败:${error.detail}`;
          console.error('请求失败:', error.detail);
          Message.error({
            message: `删除评论失败：${error_info}`,
            duration: 3000
          });
        }
      }
    }
  }
};
</script>

<style scoped>
.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100px;
}
.loading-container span {
  margin-left: 10px;
}
.error-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100px;
  color: red;
}
.error-icon {
  margin-right: 10px;
}
</style>
