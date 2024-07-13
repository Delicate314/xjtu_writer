# 后端
python = 3.10
## 配置虚拟环境
pip install -r requirements.txt

## 进入虚拟环境
cd /home
source venv/bin/activate

## 启动服务器
uvicorn sql_app.main:app --reload --port 8000