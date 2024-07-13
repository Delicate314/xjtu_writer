# xjtu_writer
## 运行nginx
### ubuntu激活虚拟环境：
cd /home
source venv/bin/activate
### 启动命令
cd /home/xjtu_writer/xjtu_writer/back_end
uvicorn sql_app.main:app --reload --port 8000
后台启动
nohup uvicorn sql_app.main:app --reload --port 8000 &
后台停止
ps -aux | grep "runoob.sh" 找到nohup的进程pid
kill -9  进程号PID
### 在浏览器访问云服务器上的文档
http://121.36.55.149/docs
