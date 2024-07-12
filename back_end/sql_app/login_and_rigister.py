import pymysql
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
import re
from fastapi.middleware.cors import CORSMiddleware

class UserRegister(BaseModel):  # 继承BaseModel类，方便正则表达式检查
    user_name: str
    user_pwd: str


class UserLogin(BaseModel):
    user_name: str
    user_pwd: str

# @app.post("/register")
def register(user_register: UserRegister):
    db = pymysql.connect(
        host="114.55.130.178",  # MySQL服务器地址
        user="user01",  # 用户名
        password="20030704Liwan",  # 密码
        database="novel_ai",
        port=3306  # 数据库端口
    )

    cursor = db.cursor()
    sql_check = "SELECT * FROM user_info WHERE user_name = %s;"  # 检查注册是否重复
    value = (user_register.user_name,)

    cursor.execute(sql_check, value)
    check_result = cursor.fetchone()
    if check_result is None:  # 没有重复
        sql_insert = "INSERT INTO user_info (user_name, user_password) VALUES (%s, %s)"
        values = (user_register.user_name, user_register.user_pwd)
        cursor.execute(sql_insert, values)
        db.commit()
    else:
        cursor.close()
        db.close()
        raise HTTPException(status_code=400, detail="用户名重复，请重新输入！")

    cursor.close()  # 关闭游标
    db.close()  # 关闭数据库连接

    return {
        "msg": "注册成功！",
        "success": True,
    }

# @app.post("/login")
def login(user_login: UserLogin):
    db = pymysql.connect(
        host="114.55.130.178",  # MySQL服务器地址
        user="user01",  # 用户名
        password="20030704Liwan",  # 密码
        database="novel_ai",
        port=3306  # 数据库端口
    )

    cursor = db.cursor()
    sql_check = "SELECT user_password FROM user_info WHERE user_name = %s;"
    value = (user_login.user_name,)

    cursor.execute(sql_check, value)
    result = cursor.fetchone()

    sql_id = "SELECT user_id FROM user_info WHERE user_name = %s;"

    cursor.execute(sql_id, value)
    result2 = cursor.fetchone()

    print("sql_user_id")
    print(result2[0])

    cursor.close()  # 关闭游标
    db.close()  # 关闭数据库连接

    if result is None:
        raise HTTPException(status_code=400, detail="网络出现问题，请重试!")
    
    stored_password = result[0]
    if user_login.user_pwd != stored_password:
        raise HTTPException(status_code=400, detail="用户名或密码错误！")

    return {
        "user_id": result2[0],
        "msg": "登录成功！",
        "success": True
    }
