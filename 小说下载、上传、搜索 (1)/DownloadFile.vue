<template>
    <div>
      <button @click="downloadFile">Download File</button>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'FileDownload',
    methods: {
      async downloadFile() {
        try {
          const novelId = '16'; // 替换为实际的 novel_id
          const response = await axios.get(`http://127.0.0.1:8000/apis/downloadfile`, {
            params: {
              novel_id: novelId
            },
            responseType: 'blob' // 指定响应类型为 blob
          });
  
          // 创建一个 URL 对象指向 blob
          const url = window.URL.createObjectURL(new Blob([response.data]));
  
          // 创建一个临时的链接元素
          const link = document.createElement('a');
          link.href = url;
  
          // 从响应头中提取文件名
          const contentDisposition = response.headers['content-disposition'];
          let filename = 'download.txt'; // 默认文件名
  
          if (contentDisposition) {
            const filenameMatch = contentDisposition.match(/filename="?(.+)"?/);
            if (filenameMatch.length === 2) {
              filename = filenameMatch[1];
            }
          }
  
          link.setAttribute('download', filename);
          document.body.appendChild(link);
  
          // 自动点击链接以触发下载
          link.click();
  
          // 移除临时链接元素
          document.body.removeChild(link);
        } catch (error) {
          console.error('Error downloading file:', error);
        }
      }
    }
  };
  </script>
  
  <style scoped>
  button {
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  </style>
  