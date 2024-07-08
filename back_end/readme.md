# 后端
python = 3.10
## 配置虚拟环境
pip install -r requirements.txt

## 启动服务器
uvicorn sql_app.main:app --reload --port 8000