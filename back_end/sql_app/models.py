import pymysql
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
import re

# 建表
class UserRegister(BaseModel):  # 继承BaseModel类，方便正则表达式检查
    user_name: str
    user_pwd: str

    @field_validator("user_name")  # 检查用户名
    def user_name_must(cls, value):
        r = '^[a-zA-Z\d]{1,20}$'
        result = re.match(r, value)
        if result is None:
            raise ValueError('要求为1-20位字母、数字的组合！')
        return value

    @field_validator("user_pwd")  # 检查密码
    def user_pwd_must(cls, value):
        r = '^(?:(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])).{5,10}$'
        result = re.match(r, value)
        if result is None:
            raise ValueError('要求6-10位密码，含有数字、大小写字母!')
        return value

class UserLogin(BaseModel):
    user_name: str
    user_pwd: str