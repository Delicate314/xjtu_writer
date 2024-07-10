const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave: false,  // 关闭语法检查
  devServer: {  // 开发环境服务配置
    proxy: {  //跨域
      '/api': {  // 标识
        target: 'http://localhost:8000/',  // 目标服务器
        ws: true,  // 支持 webscoket
        changeOrigin: true,  // 是否跨域
        pathRewrite: { "^/api": "" }  // 重写请求地址
      },
    }
  }
})