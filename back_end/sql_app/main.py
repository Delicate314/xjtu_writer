from fastapi import Depends, FastAPI, HTTPException, UploadFile, status, Form, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import InvalidTokenError
import jwt
from . import ai01, ai02, login_and_rigister, models, db_method, novel_option
from pydantic import BaseModel
import re
from .file_option import *
from .search_novel import *

import pymysql


class Write_request(BaseModel):
    contents: str
class Answer_request(BaseModel):
    question: str
    context: str



SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"     #密钥
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 100          #这是token有效期，这里表示1分组，如果超过这个时间，需要重新登录，先设置为1方便测试


class Write_request(BaseModel):
    contents: str
class Answer_request(BaseModel):
    question: str
    context: str
    
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="apis/login")     #在登录的那个路径下会给oauth2_scheme赋值
'''
get_current_user函数是用来登陆后，如果用户想要进行其他操作，这个时候，用这个函数，它会验证token是否有效、token是否过期，返回为user_id，方便
后续使用。此外，如果某些功能需要登陆后才能使用，那么必须使用这个函数进行判断，使用方法只需要在原来的基础上，增加一个参数，例如：
以获取排行榜为例：
原来为：
async def rank(index:int):
修改后：
async def rank(index:int,user:str=Depends(get_current_user)):
多加了user:str=Depends(get_current_user)，其余函数一样
'''
async def get_current_user(token: str = Depends(oauth2_scheme)):    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # print(payload)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        #  token_data = TokenData(username=username)
    except InvalidTokenError:
        # print("111")
        raise credentials_exception
    db = get_db()
    # print(Header())
    cursor = db.cursor()
    sql_select="SELECT * FROM user_info WHERE user_name= %s;"
    value=(username,)
    result=cursor.execute(sql_select,value)
    # user = get_user(fake_users_db, username=token_data.username)
    cursor.close()  # 关闭游标
    db.close()  # 关闭数据库连接
    if result ==0:
        raise credentials_exception
    return username

async def get_current_user_id(token: str = Depends(oauth2_scheme)):    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    
    db = get_db()
    
    cursor = db.cursor()
    sql_select = "SELECT * FROM user_info WHERE user_name = %s;"
    value = (username,)
    cursor.execute(sql_select, value)
    
    user_info = cursor.fetchone()  # 获取查询结果
    
    cursor.close()  # 关闭游标
    db.close()  # 关闭数据库连接
    
    if user_info is None:
        raise credentials_exception
    
    # 假设你想获取 user_info 中的某个字段，比如 user_id
    user_id = str(user_info['user_id'])  # 使用列名访问字段
    
    return user_id


@app.post("/apis/register",tags=["用户注册"],summary="用户注册")
async def register(user_register: models.UserRegister):
    message = login_and_rigister.register(user_register)
    return message

@app.post("/apis/login", tags=["用户登录"],summary="用户向服务器发送登录请求")  
async def login(user_login: OAuth2PasswordRequestForm= Depends()):
    message = login_and_rigister.login(user_login)
    return message

DIR = "/home/xjtu_writer/xjtu_writer/novel"
@app.post(path="/apis/uploadfile", tags=["上传文件"], description="""
          用户上传文件\n
          只支持txt文件\n
          文件存储位置: DIR/user_id/novel_id.txt\n""")
async def upload_file(
    file: UploadFile = File(...),
    novel_title: str = Form(...),
    user_id: str = Depends(get_current_user_id)
):
    return await novel_option.upload_file(file, novel_title, user_id)

@app.post(path="/apis/downloadfile", tags=["下载文件"], summary="下载小说文件")
async def download_file(input: novel_option.Novel, user:str=Depends(get_current_user)):
    return await novel_option.download_file(input)

@app.post(path="/apis/getNovel", tags=["获取小说内容"],
         description ="""获取小说内容展示在终端\n
         注意：当前有效小说id为1到5\n
         可以自己上传文件测试\n
         输入为小说id、获取的页数、获取的页大小\n
         这里的页大小指的是行数""")
async def show_file(input: novel_option.GetNovel, user:str=Depends(get_current_user)):
    return await novel_option.show_file(input)

@app.post(path="/apis/search", summary = "搜索小说", description="""
         可以通过作者id、作者名、小说id、小说关键字查询小说.\n
         func = 0: 通过关键字查询(对小说名和小说简介进行部分匹配)\n
         func = 1: 通过小说id查询\n
         func = 2: 通过作者id查询\n
         func = 3: 通过作者名查询(不区分大小写，可以部分匹配)\n
         func = 其他:\n
         返回值：\n
         status_code: 0表示正确，1表示错误\n""", tags=["搜索"])
async def search_novel(input : novel_option.SearchNovel ,user:str=Depends(get_current_user)):
    return await novel_option.search_novel(input)

class rank_input(BaseModel):
    index : int

@app.post("/apis/rank", tags=["获取排行榜"], summary="获取排行榜，输入参数index", description="index为1表示排行1-10，为2表示排行11-20，以此类推")
#async def rank(index: int, user: str = Depends(get_current_user)):
async def rank(input: rank_input ,user:str=Depends(get_current_user)):

    index = input.index
    db = get_db()
    cursor = db.cursor(pymysql.cursors.DictCursor)  # 使用字典游标
    select_rank_sql = """
    SELECT
        novel_info.novel_id,
        novel_info.novel_title,
        novel_info.user_id,
        novel_info.novel_viewcount,
        user_info.user_name
    FROM novel_info
    JOIN user_info ON novel_info.user_id = user_info.user_id
    ORDER BY novel_info.novel_viewcount DESC
    LIMIT %s, 10
    """
    offset = (index - 1) * 10
    cursor.execute(select_rank_sql, (offset,))
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result

# @app.post("/apis/model/change", tags=["模型切换"],summary="用户向服务器发送模型切换请求")
# async def change_model(model:str):
#     message = "模型切换成功"
#     return {message}

@app.post(path="/apis/importNovel", tags=["导入小说"], description="""
          \n用户上传文件\n
          直接返回文件内容\n""")
async def import_file(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user_id)
):
    return await novel_option.import_file(file, user_id)

@app.post(path="/apis/novel/releaseNovel", tags=["发布小说"], description="""
          \n用户上传小说，str\n
          """)
async def release_novel(
    novel: str = Form(...),
    user_id: str = Depends(get_current_user_id),
    novel_title: str = Form(...)
):
    return await novel_option.release_novel(novel, user_id, novel_title)

@app.post("/apis/write_request", tags=["AI写小说"],summary="用户向服务器发送AI写小说请求")
async def ai_write_novel(contents:Write_request ):
    contents = contents.contents
    response = ai01.call_with_messages(contents)
    return response

@app.post("/apis/answer_request", response_model=str , tags=["AI回答问题"],summary="用户向服务器发送让AI回答问题的请求")
async def ai_answer_question(question:Answer_request):
    question1 = question.question
    context = question.context
    response = ai02.call_with_messages(question1,context)
    return response



def is_valid_password(password: str) -> bool:
    # 检查长度
    if len(password) < 6 or len(password) > 20:
        return False

    # 检查是否包含数字、小写字母和大写字母
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[A-Z]", password):
        return False

    return True

@app.post("/apis/admin/changepwd", tags=['超级用户权限'], summary='修改Admin密码',
          description='需要旧密码和新密码，仅能修改超级用户的密码')
async def admin_change_password(user_password: str, user_newpassword: str):
    # 调用数据库方法获取管理员信息
    Admin = db_method.get_user_info(0, 'Admin')
    if not Admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="未知数据库错误"
        )
    old_password = Admin[0][2]

    if old_password != user_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="密码错误"
        )

    if not is_valid_password(user_newpassword):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="新密码格式错误, 要求6-20位密码，含有数字、大小写字母!"
        )

    try:
        (success, info) = db_method.change_pwd(0, 'Admin', user_newpassword)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update password: {str(info)}"
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update password: {str(e)}"
        )

    return {"message": "修改密码成功"}

@app.get("/apis/admin/getNovel",tags=['超级用户权限'], summary='得到搜索目标或所有小说信息',
         description="""
参数说明:\n
    --offset:偏移量 & row_count:一次得到的总行数\n
    --order_by:以某列排序(默认novel_id) & order_way:排序方式(默认:升序acs/ascending;降序desc/descending)\n
    --search_target:搜索关键词,自动搜索novel_id,user_id和novel_title匹配的项目,不填写为全部元组\n
返回小说信息和搜索到的总数\n
         """)
async def admin_get_all_novel(offset: int, row_count: int, order_by='novel_id', order_way='asc', search_target='all'):
    try:
        if order_way == 'ascending':
            order_way = 'asc'
        if order_way == 'descending':
            order_way = 'desc'
        response = db_method.get_all_novel_info(row_count, offset, order_by, order_way,search_target)
        num = db_method.get_novel_count(search_target=search_target)
        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="数据库内没有小说"
            )
        data = []
        novel_links = []

        for row in response:
            row_data = {
                'novel_id': row[0],
                'user_id': row[1],
                'novel_title': row[2],
                'novel_description': row[3],
                'UpdatedAt': '-' if len(row) < 7 else row[6],
                'novel_viewcount': row[5]
            }
            row_link = {
                'novel_id': row[0],
                'novel_path': row[4]
            }
            data.append(row_data)
            novel_links.append(row_link)

        return {"data": data, "novel_links": novel_links, "count":num}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching novel information: {str(e)}"
        )

@app.get("/apis/admin/getusers",tags=['超级用户权限'], summary='得到搜索目标或所有用户信息',
         description="""
参数说明:\n
    --offset:偏移量 & row_count:一次得到的总行数\n
    --order_by:以某列排序(默认user_id) & order_way:排序方式(默认:升序acs/ascending;降序desc/descending)\n
    --search_target:搜索关键词,自动搜索user_id和user_name匹配的项目,不填写为全部元组\n
返回用户信息和搜索到的总数\n
""")
async def admin_get_all_user(offset: int, row_count: int, order_by='user_id', order_way='asc', search_target='all'):
    try:
        if order_way == 'ascending':
            order_way = 'asc'
        if order_way == 'descending':
            order_way = 'desc'
        response = db_method.get_all_user_info(one_length=row_count, offset=offset, order_by=order_by,
                                               order_way=order_way, search_target=search_target)
        num = db_method.get_user_count(search_target=search_target)
        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="数据库内没有用户"
            )
        data = []

        for row in response:
            row_data = {
                'user_id': row[0],
                'user_name': row[1],
                'CreateAt': '-' if len(row) < 4 else row[3],
                'UpdatedAt': '-' if len(row) < 5 else row[4],
            }
            data.append(row_data)

        return {'users': data, 'count': num}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching novel information: {str(e)}"
        )

@app.delete("/apis/admin/deleteuser",tags=['超级用户权限'], summary='删除用户', description="""
参数说明:\n
    --user_id:需要删除的用户id\n
    --user_name:需要删除的用户名\n
""")
async def admin_delete_user(user_name: str, user_id: str):
    user_id = int(user_id)
    (s, msg) = db_method.delete_user(user_id=user_id, user_name=user_name)
    if s == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=msg
        )
    if s == 1:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=msg
        )
    return {'message': msg}

@app.delete("/apis/admin/deletenovel", tags=['超级用户权限'], summary='删除小说', description="""
参数说明:\n
    --novel_id:需要删除的小说id\n
    --novel_title:需要删除的小说名\n
""")
async def admin_delete_novel(novel_id: int, novel_title: str):
    (s, msg) = novel_option.delete_novel(novel_id, novel_title)
    if s == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=msg
        )
    if s == 1:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=msg
        )
    return {'message': msg}

@app.post("/apis/admin/resetpassword",tags=['超级用户权限'], summary='重置用户密码', description="""
参数说明:\n
    --user_id:用户id\n
    --user_name:用户名\n
""")
async def admin_reset_password(user_name: str, user_id: str):
    user_id = int(user_id)
    (s, m) = db_method.reset_password(user_id, user_name)
    if not s:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=m
        )
    return {'message': m}

@app.get("/apis/admin/getusernovel", tags=['超级用户权限'], summary='查找某个用户发布的小说', description="""
参数说明:
    user_id:用户名
返回:小说""")
async def admin_get_user_novel(user_id: str):
    try:
        rows = db_method.get_user_novel(user_id)

        count = 0
        data = []

        for row in rows:
            count+=1
            row_data = {
                'novel_id': row[0],
                'user_id': row[1],
                'novel_title': row[2],
                'novel_description': row[3],
                'UpdatedAt': '-' if len(row) < 7 else row[6],
                'novel_viewcount': row[5]
            }
            row_link = {
                'novel_id': row[0],
                'novel_path': row[4]
            }
            data.append(row_data)

        return {"data": data, "count": count}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching novel information: {str(e)}"
        )