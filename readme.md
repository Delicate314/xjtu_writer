# xjtu_writer
## 运行nginx
### ubuntu激活虚拟环境：
cd /home
source venv/bin/activate
### 启动命令
cd /home/demoAPI
uvicorn sql_app.main:app --reload --port 8000
### 在浏览器访问云服务器上的文档
http://121.36.55.149/docs
