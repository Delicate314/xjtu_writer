<template>
    <el-dialog 
    :visible.sync="visible" 
    @close="handleClose"
    width="63%"
    :style="{ 'max-height': '80vh' }"
    :append-to-body="true">
        <template #title>
            用户{{ detailData.user_name }}的详细信息
        </template>
        <div class="info-title">已发布的小说: (共{{ novelCount }}部)</div>
        <el-table :data="dialogData" v-loading="loading" element-loading-text="加载中...">
            <el-table-column fixed prop="novel_id" label="小说id" width="120"></el-table-column>
            <el-table-column prop="user_id" label="用户id" width="120"></el-table-column>
            <el-table-column prop="novel_title" label="小说标题" width="150"></el-table-column>
            <el-table-column prop="novel_description" label="小说简介" width="380"></el-table-column>
            <el-table-column prop="UpdatedAt" label="更新时间" width="150"></el-table-column>
            <el-table-column prop="novel_viewcount" label="浏览量" width="100"></el-table-column>
        </el-table>
    </el-dialog>
</template>

<script>
import { Message } from 'element-ui';

export default {
  props: {
    visible: {
      type: Boolean,
      required: true
    },
    detailData: {
      type: Object,
      required: true
    }
  },

  data() {
    return {
      dialogData: [],
      novelCount: 0,
      loading: false,
      // url_api:'127.0.0.1:8000',
      url_api:'121.36.55.149/apis',
    };
  },
  
  watch: {
    detailData: {
      immediate: true,
      handler() {
        this.fetchUserNovels();
      }
    }
  },

  methods: {
    handleClose() {
      this.$emit('update:visible', false);
    },
    
    async fetchUserNovels() {
      const uid = this.detailData.user_id;
      this.loading = true;
      try {
        const url = `http://${this.url_api}/admin/getusernovel?user_id=${uid}`;
        const response = await fetch(url, { timeout: 8000 });
        const responseData = await response.json();
        this.dialogData = responseData.data;
        this.novelCount = responseData.count;
      } catch (error) {
        console.error('获取小说信息失败:', error);
        Message.error({
          message: `获取小说信息失败: ${error.message || '未知错误'}`,
          duration: 3000
        });
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.info-title {
  margin-left: 10px;
  text-align: left;
  font-size: small;
}
</style>
