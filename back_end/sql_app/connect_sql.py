import pymysql

def get_db():
    # 创建数据库连接
    db = pymysql.connect(
    host="114.55.130.178",  # MySQL服务器地址
    user="user01",
    password="20030704Liwan",  # 密码
    database="novel_ai"  # 数据库名称
    )
    return db

def get_cursor(db):
    return db.cursor()