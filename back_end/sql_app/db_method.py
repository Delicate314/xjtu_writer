from .connect_sql import get_cursor,get_db
import pymysql
from . import search_novel
from . import novel_option

def get_user_info(id: int, name: str):
    sql = "SELECT * FROM user_info WHERE user_name='admin'"
    db = get_db()
    cursor = get_cursor(db)
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    
    return rows


def get_all_user_info(one_length=0, offset=-1, order_by='user_id', order_way='asc', search_target='all'):
    db = get_db()
    cursor = get_cursor(db)

    # Validate order_way to prevent SQL injection
    order_way = order_way.lower()
    if order_way not in ['asc', 'desc']:
        order_way = 'desc'

    # Construct search condition with parameterized query to prevent SQL injection
    if search_target == 'all' or not search_target.strip():
        search = ""
        search_params = []
    else:
        if search_target.isdigit():
            search = "AND (user_id = %s OR user_name LIKE %s)"
            search_params = [search_target, f"%{search_target}%"]
        else:
            search = "AND user_name LIKE %s"
            search_params = [f"%{search_target}%"]

    # Build SQL query based on offset and one_length
    if offset == -1 or one_length == 0:
        sql = f"SELECT * FROM user_info WHERE user_name<>'admin' {search} ORDER BY {order_by} {order_way}"
        cursor.execute(sql, search_params)
    else:
        sql = f"SELECT * FROM user_info WHERE user_name<>'admin' {search} ORDER BY {order_by} {order_way} LIMIT %s OFFSET %s"
        cursor.execute(sql, search_params + [one_length, offset])

    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return rows

def change_pwd(user_id:int, user_name:str, new_password:str):
    try:
        db = get_db()
        cursor = get_cursor(db)
        # 准备 SQL 更新语句
        sql_update_query = "UPDATE user_info SET user_password = %s WHERE user_name = %s"
        # 执行更新操作
        cursor.execute(sql_update_query, (new_password, user_name))
        # 提交事务
        cursor.connection.commit()
        return (True, f"修改管理员密码成功")
    except Exception as e:
        print("f")
        return (False, f"发生错误{e}")
    finally:
        print("t")
        cursor.close()
        db.close()

    return (True,"success")


def get_all_novel_info(one_length=0, offset=-1, order_by='novel_id', order_way='asc', search_target='all'):
    db = get_db()
    cursor = get_cursor(db)
    order_way = order_way.lower()
    if order_way not in ['asc', 'desc']:
        order_way = 'asc'

    if search_target == 'all' or not search_target.strip():
        search = ""
        search_params = []
    else:
        if search_target.isdigit():
            search = "WHERE user_id = %s OR novel_id = %s OR novel_title LIKE %s"
            search_params = [search_target, search_target, f"%{search_target}%"]
        else:
            search = "WHERE novel_title LIKE %s"
            search_params = [f"%{search_target}%"]

    if offset == -1 or one_length == 0:
        sql = f"SELECT * FROM novel_info {search} ORDER BY {order_by} {order_way}"
        cursor.execute(sql, search_params)
    else:
        sql = f"SELECT * FROM novel_info {search} ORDER BY {order_by} {order_way} LIMIT %s OFFSET %s"
        cursor.execute(sql, search_params + [one_length, offset])

    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return rows

def get_user_count(search_target='all'):
    if search_target == 'all' or not search_target.strip():
        search = ""
        search_params = []
    else:
        if search_target.isdigit():
            search = "AND (user_id = %s OR user_name LIKE %s)"
            search_params = [search_target, f"%{search_target}%"]
        else:
            search = "AND user_name LIKE %s"
            search_params = [f"%{search_target}%"]
    db=get_db()
    cursor = get_cursor(db)
    sql = f"SELECT count(*) FROM user_info WHERE user_name<>'admin' {search}"
    cursor.execute(sql, search_params)
    rows = cursor.fetchall()[0]
    return rows


def get_novel_count(search_target='all'):
    if search_target == 'all' or not search_target.strip():
        search = ""
        search_params = []
    else:
        if search_target.isdigit():
            search = "WHERE user_id = %s OR novel_id = %s OR novel_title LIKE %s"
            search_params = [search_target, search_target, f"%{search_target}%"]
        else:
            search = "WHERE novel_title LIKE %s"
            search_params = [f"%{search_target}%"]

    db = get_db()
    cursor = get_cursor(db)
    sql = f"SELECT count(*) FROM novel_info  {search}"
    cursor.execute(sql, search_params)
    count = cursor.fetchone()[0]  # 获取计数值
    cursor.close()
    db.close()
    return count

def delete_user(user_id:int, user_name:str):
    try:
        db = get_db()
        cursor = get_cursor(db)  # 获取数据库游标
        #删除该用户所有小说
        user_novels = get_user_novel(user_id)
        for novel in user_novels:
            novel_option.delete_novel(novel[0], novel[2])
        # 执行删除操作
        delete_sql = "DELETE FROM user_info WHERE user_id = %s AND user_name = %s"
        cursor.execute(delete_sql, (user_id, user_name))
        # 检查是否成功删除
        if not cursor.rowcount:
            return (0, '用户未找到或不存在')
        # 提交事务
        cursor.connection.commit()

    except Exception as e:
        cursor.connection.rollback()  # 回滚事务
        return (1, f"An error occurred while deleting the user: {str(e)}")

    finally:
        cursor.close()  # 确保关闭游标
        db.close()

    return (2, "用户删除成功")

def delete_novel(novel_id:int, novel_name:str):
    try:
        db = get_db()
        cursor = get_cursor(db)  # 获取数据库游标
        # 执行删除操作
        delete_sql = "DELETE FROM novel_info WHERE novel_id = %s AND novel_title = %s"
        cursor.execute(delete_sql, (novel_id, novel_name))
        # 检查是否成功删除
        if not cursor.rowcount:
            return (0, '小说未找到或不存在')
        # 提交事务
        cursor.connection.commit()

    except Exception as e:
        cursor.connection.rollback()  # 回滚事务
        return (1, f"An error occurred while deleting the user: {str(e)}")

    finally:
        cursor.close()  # 确保关闭游标
        db.close()

    return (2, "小说删除成功")

def reset_password(user_id: int, user_name: str):
    try:
        default_password = '123456Ab'
        db = get_db()
        cursor = get_cursor(db)
        # 查找用户并更新密码的SQL语句
        sql = "UPDATE user_info SET user_password=%s WHERE user_id=%s AND user_name=%s"
        # 执行SQL语句
        cursor.execute(sql, (default_password, user_id, user_name))
        cursor.connection.commit()
        return (True, f"用户 {user_name} 的密码已被重置为 {default_password}")
    except Exception as e:
        return (False, f"发生错误{e}")
    finally:
        cursor.close()
        db.close()

def get_user_info(user_id: int):
    db = get_db()
    cursor = get_cursor(db)
    query = "SELECT * FROM user_info WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    user_info = cursor.fetchall()
    cursor.close()
    db.close()
    return user_info

def get_user_novel(user_id:int):
    db = get_db()
    cursor = get_cursor(db)
    query = "SELECT * FROM novel_info WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    novels = cursor.fetchall()
    cursor.close()
    db.close()
    return novels

def get_novel_comment(novel_id:int):
    db = get_db()
    cursor = get_cursor(db)
    query = "SELECT * FROM comment WHERE novel_id = %s"
    cursor.execute(query, (novel_id,))
    comments = cursor.fetchall()
    cursor.close()
    db.close()
    return comments



def get_novel_comment_admin(novel_id: int):
    db = get_db()
    cursor = get_cursor(db)
    query = "SELECT * FROM comment WHERE novel_id = %s"
    cursor.execute(query, (novel_id,))
    result = cursor.fetchall()
    comments = [
        {
            "comment_id": row[0],
            "comment_content": row[1],
            "user_id": row[2],
            "novel_id": row[3],
            "updateAt": row[4].isoformat()
        }
        for row in result
    ]
    cursor.close()
    return {'data': comments}

def delete_comment(comment_id:int):
    try:
        db = get_db()
        cursor = get_cursor(db)  # 获取数据库游标
        # 执行删除操作
        delete_sql = "DELETE FROM comment WHERE comment_id = %s"
        cursor.execute(delete_sql, (comment_id,))
        # 检查是否成功删除
        if not cursor.rowcount:
            return (0, '评论未找到或不存在')
        # 提交事务
        cursor.connection.commit()

    except Exception as e:
        cursor.connection.rollback()  # 回滚事务
        return (1, f"An error occurred while deleting the comment: {str(e)}")

    finally:
        cursor.close()  # 确保关闭游标
        db.close()

    return (2, "评论删除成功")
