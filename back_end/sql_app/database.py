import pymysql

def connect_db():
    db = pymysql.connect(
        host="114.55.130.178",  # MySQL服务器地址
        user="user01",  # 用户名
        password="20030704Liwan",  # 密码
        database="novel_ai",
        port=3306  # 数据库端口
    )
    return db