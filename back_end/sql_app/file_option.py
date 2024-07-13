import pymysql
from .connect_sql import get_db

# 执行插入操作并获取小说的id
def insert_novel_to_sql(user_id, novel_title, novel_path, novel_description = None):
    sql = """
    INSERT INTO novel_info (user_id, novel_title, novel_path, novel_description)
    VALUES (%s, %s, %s, %s);
    """
    db = get_db()
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
    
# 执行插入操作并获取小说的id
def insert_novel_to_sql(user_id, novel_title, novel_path, novel_description = None):
    sql = """
    INSERT INTO novel_info (user_id, novel_title, novel_path, novel_description)
    VALUES (%s, %s, %s, %s);
    """
    db = get_db()
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