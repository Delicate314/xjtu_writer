import mysql.connector
import json

#将字典列表转成json
def tuples_to_json(str_keys, tuples):  
    # 初始化一个空列表，用于存放转换后的字典  
    result = []  
    
    # 遍历元组列表  
    for tup in tuples:  
        # 创建一个字典，键为str_keys中的元素，值为元组中的对应项  
        # 使用zip函数将str_keys和元组中的元素配对，然后使用dict函数创建字典  
        d = dict(zip(str_keys, tup))  
        # 将这个字典添加到结果列表中  
        result.append(d)  
    
    #将字典转成json
    result = json.dumps(result, ensure_ascii=False, indent=4) 
    return result 

# 连接到 MySQL 数据库
def create_connection():
    return mysql.connector.connect(
        host="114.55.130.178",  # MySQL服务器地址
        user="user01",   # 用户名
        password="20030704Liwan",  # 密码
        database="novel_ai"  # 数据库名称
    )


#查询所有小说名和小说描述中包含keyword的小说
def search_novel_by_keyword(keyword):
    sql = """
    SELECT 
        n.novel_id, 
        n.novel_title, 
        n.novel_description, 
        n.novel_path, 
        n.novel_viewcount, 
        ui.user_id, 
        ui.user_name
    FROM 
        novel_info n
    LEFT JOIN 
        user_info ui
    ON 
        n.user_id = ui.user_id
    WHERE 
        n.novel_title LIKE %s OR
        n.novel_description LIKE %s;
    """
    values = (f"%{keyword}%", f"%{keyword}%")
    db = create_connection()
    try:
        # 创建游标对象，用于执行SQL查询
        cursor = db.cursor()
        cursor.execute(sql, values)
        result = cursor.fetchall()
        result = tuples_to_json(["novel_id", "novel_title", "novel_description", "novel_path", "novel_viewcount", "user_id", "user_name"], result)
        return result
    finally:
        db.close()


#根据小说id查询对应所有小说
def search_novel_by_novel_id(writer_id):
    sql = """
    SELECT 
    *
FROM 
    novel_info n
WHERE 
    n.novel_id = %s;
    """
    values = (writer_id,)
    db = create_connection()
    try:
        # 创建游标对象，用于执行SQL查询
        cursor = db.cursor()
        cursor.execute(sql, values)
        result = cursor.fetchall()
        result = tuples_to_json(["novel_id", "user_id", "novel_title", "novel_description", "novel_path", "novel_viewcount"], result)
        return result
    finally:
        db.close()

#根据作者id查询对应所有小说
def search_novel_by_writer_id(writer_id):
    sql = """
    SELECT 
    *
FROM 
    novel_info n
WHERE 
    n.user_id = %s;
    """
    values = (writer_id,)
    db = create_connection()
    try:
        # 创建游标对象，用于执行SQL查询
        cursor = db.cursor()
        cursor.execute(sql, values)
        result = cursor.fetchall()
        result = tuples_to_json(["novel_id", "user_id", "novel_title", "novel_description", "novel_path", "novel_viewcount"], result)
        return result
    finally:
        db.close()