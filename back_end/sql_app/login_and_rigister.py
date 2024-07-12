import pymysql
from fastapi import FastAPI, HTTPException,Depends
from pydantic import BaseModel, Field, field_validator
import re
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from datetime import timedelta,timezone,datetime
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1
class UserRegister(BaseModel):  # 继承BaseModel类，方便正则表达式检查
    user_name: str
    user_pwd: str


class UserLogin(BaseModel):
    user_name: str
    user_pwd: str

'''
下边这个函数为创建token，在登录的时候使用，会设置过期时间，最后对user_id，时间进行加密，因此不同时间获得的token是不同的
'''
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    print(to_encode)
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=1)
    to_encode.update({"exp": expire})
    print(to_encode)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

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
        # raise HTTPException(status_code=400, detail="用户名重复，请重新输入！")
        return {
        "msg": "用户名重复！",
        "success": False,
        }

    cursor.close()  # 关闭游标
    db.close()  # 关闭数据库连接

    return {
        "msg": "注册成功！",
        "success": True,
    }

# @app.post("/login")
def login(user_login: OAuth2PasswordRequestForm= Depends()):
    db = pymysql.connect(
        host="114.55.130.178",  # MySQL服务器地址
        user="user01",  # 用户名
        password="20030704Liwan",  # 密码
        database="novel_ai",
        port=3306  # 数据库端口
    )

    cursor = db.cursor()
    sql_check = "SELECT user_password FROM user_info WHERE user_name = %s;"
    value = (user_login.username,)

    cursor.execute(sql_check, value)
    result = cursor.fetchone()

    sql_id = "SELECT user_id FROM user_info WHERE user_name = %s;"

    cursor.execute(sql_id, value)
    result2 = cursor.fetchone()

    is_admin = "SELECT is_admin FROM user_info WHERE user_name = %s;"

    cursor.execute(is_admin, value)
    result3 = cursor.fetchone()
    cursor.close()  # 关闭游标
    db.close()  # 关闭数据库连接

    if result is None:
        raise HTTPException(status_code=400, detail="用户名或密码错误！")
    
    stored_password = result[0]
    if user_login.password != stored_password:
        raise HTTPException(status_code=400, detail="用户名或密码错误！")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_login.username}, expires_delta=access_token_expires
    )
    return {
        "is_admin": result3[0],
        "user_id": result2[0],
        "msg": "登录成功！",
        "success": True,
        "access_token": access_token, "token_type": "bearer"
    }
