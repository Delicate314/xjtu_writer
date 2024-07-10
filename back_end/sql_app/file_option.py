from .search_novel import create_connection
import pymysql
# 执行插入操作并获取小说的id
def insert_novel_to_sql(user_id, novel_title, novel_path, novel_description = None):
    sql = """
    INSERT INTO novel_info (user_id, novel_title, novel_path, novel_description)
    VALUES (%s, %s, %s, %s);
    """
    db = pymysql.connect(
        host="114.55.130.178",  # MySQL服务器地址
        user="user01",  # 用户名
        password="20030704Liwan",  # 密码
        database="novel_ai",
        port=3306  # 数据库端口
    )
    novel_id = None
    try:
        cursor = db.cursor()
        values = (user_id, novel_title, novel_path, novel_description)
        cursor.execute(sql, values)
        db.commit()
        novel_id = cursor.lastrowid
    except pymysql.Error as err:
        print(f"Error: {err}")
        db.rollback()
        return None
    finally:
        cursor.close()
        db.close()
        return novel_id