from fastapi import Depends, FastAPI, HTTPException, UploadFile, status, Query, Form, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException, UploadFile, status, Query, Form, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import FileResponse, JSONResponse
from fastapi.responses import FileResponse, JSONResponse
from jwt import InvalidTokenError
import jwt
from sqlalchemy.orm import Session
from . import ai01, ai02, login_and_rigister, models, db_method
from pydantic import BaseModel
import os, shutil, re
import logging
from .file_option import *
from .search_novel import *


# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Write_request(BaseModel):
    contents: str
class Answer_request(BaseModel):
    question: str
    
from fastapi.staticfiles import StaticFiles
from . import schemas, ai01, ai02, login_and_rigister, models
from pydantic import BaseModel
import os, shutil
import urllib.parse
import logging
from .file_option import *
from .search_novel import *
import pymysql
from datetime import timedelta,timezone,datetime


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"     #密钥
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1          #这是token有效期，这里表示1分组，如果超过这个时间，需要重新登录，先设置为1方便测试


# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Write_request(BaseModel):
    contents: str
class Answer_request(BaseModel):
    question: str
    
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




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
    db = pymysql.connect(
        host="114.55.130.178",  # MySQL服务器地址
        user="user01",  # 用户名
        password="20030704Liwan",  # 密码
        database="novel_ai",
        port=3306  # 数据库端口
    )
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
@app.get("/apis/rank/{index}",tags=["获取排行榜"],summary="获取排行榜，输入参数index",description="index为1表示排行1-10，为2表示排行11-20，以此类推")
async def rank(index:int,user:str=Depends(get_current_user)):
    db = pymysql.connect(
        host="114.55.130.178",  # MySQL服务器地址
        user="user01",  # 用户名
        password="20030704Liwan",  # 密码
        database="novel_ai",
        port=3306  # 数据库端口
    )
    cursor = db.cursor()
    select_rank_sql="select novel_title,user_id from novel_info  order by novel_viewcount DESC limit %s,10 "
    value=index*10-10
    # print(value)
    cursor.execute(select_rank_sql,value)
    result=cursor.fetchall()
    # print(result)
    return result
@app.post("/apis/register",tags=["用户注册"],summary="用户注册")
async def register(user_register: models.UserRegister):
    message = login_and_rigister.register(user_register)
    return message

@app.post("/apis/login", tags=["用户登录"],summary="用户向服务器发送登录请求")  
async def login(user_login: OAuth2PasswordRequestForm= Depends()):
    message = login_and_rigister.login(user_login)
    return message

DIR = "/home/xjtu_writer/xjtu_writer/novel"
@app.post("/apis/uploadfile", tags=["上传文件"], description="""
          用户上传文件\n
          只支持txt文件\n
          文件存储位置: DIR/user_id/novel_id.txt\n""")
async def upload_file(
    file: UploadFile = File(...),
    novel_title: str = Form(...),
    user_id: str = Form(...)
):
    # 判断文件类型，只支持txt文件
    if file.content_type != "text/plain":
        raise HTTPException(status_code=400, detail="Invalid file type. Only .txt files are allowed.")
    # 检查文件扩展名
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Invalid file extension. Only .txt files are allowed.")
    
    # 创建用户目录，如果不存在的话
    user_dir = os.path.join(DIR, user_id)
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)

    # 将文件插入数据库，并获取小说id
    novel_id = insert_novel_to_sql(user_id=user_id, novel_title=novel_title, novel_path=user_dir)
    if novel_id is None:
        raise HTTPException(status_code=400, detail="Insert failed, the novel id is none")
    
    # 生成文件路径
    file_path = os.path.join(user_dir, f"{novel_id}.txt")
    
    # 保存文件
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    return {"file_path": file_path, "novel_id": novel_id}

class Novel(BaseModel):
    novel_id: str

@app.post("/apis/downloadfile", tags=["下载文件"], summary="下载小说文件")
async def download_file(input: Novel):
    novel_id = input.novel_id
    try:
        # 获取小说信息
        novel_info = search_novel_by_novel_id(novel_id)
        if len(novel_info) == 0:
            raise HTTPException(status_code=404, detail="File not found")
        
        # 获取作者id用来构造文件路径
        writer_id = novel_info[0]['user_id']
        # 获取小说名用来构造文件名
        novel_title = novel_info[0]['novel_title']
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    file_path = os.path.join(DIR, str(writer_id), f"{novel_id}.txt")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    response = FileResponse(file_path, media_type='text/plain')
    # 设置文件下载时的文件名，确保支持中文文件名
    response.headers["Content-Disposition"] = f"attachment; filename*=UTF-8''{urllib.parse.quote(novel_title)}.txt"

    return response

class GetNovel(BaseModel):
    novel_id: int
    page: int = 1
    page_size: int = 10

@app.post("/apis/getNovel", tags=["获取小说内容"],
         description ="""获取小说内容展示在终端\n
         注意：目前只有小说id为1时才有数据\n
         可以自己上传文件测试\n
         输入为小说id、获取的页数、获取的页大小\n
         这里的页大小指的是行数""")
async def show_file(input: GetNovel):
    novel_id = input.novel_id
    page = input.page
    page_size = input.page_size
    try:
        #获取小说信息
        novel_info = search_novel_by_novel_id(novel_id)
        if len(novel_info) == 0:
            raise HTTPException(status_code=404, detail="File not found")
        
        # 获取作者 ID 用来构造文件路径
        writer_id = novel_info[0]['user_id']
        writer_name = novel_info[0]['user_name']
        view_count = novel_info[0]['novel_viewcount']
        novel_title = novel_info[0]['novel_title']
        
    except Exception as e:
        print(str(e))
        #raise HTTPException(status_code=500, detail=str(e))

    file_path = os.path.join(DIR, str(writer_id), f"{novel_id}.txt")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # 读取文件内容
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # 计算分页
    total_lines = len(lines)
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    paginated_lines = lines[start_index:end_index]

    # 计算总页数
    total_pages = (total_lines + page_size - 1) // page_size

    content = ''.join(paginated_lines)
    response = {
        "writer_name": writer_name,
        "view_count" : view_count,
        "novel_title": novel_title,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "total_lines": total_lines,
        "content": content
    }
    return JSONResponse(response)

class SearchNovel(BaseModel):
    func: str
    input: str

@app.post(path="/apis/search", summary = "搜索小说", description="""
         可以通过作者id、作者名、小说id、小说关键字查询小说.\n
         func = 0: 通过关键字查询(对小说名和小说简介进行部分匹配)\n
         func = 1: 通过小说id查询\n
         func = 2: 通过作者id查询\n
         func = 3: 通过作者名查询(不区分大小写，可以部分匹配)\n
         func = 其他:\n
         返回值：\n
         status_code: 0表示正确，1表示错误\n""", tags=["搜索"])
async def search_novel(input : SearchNovel):
    func = int(input.func)
    input = input.input
    match func:
        case 0:#通过关键字查询
            return {"status_code": 0 ,"result":search_novel_by_keyword(input)}
        case 1:#通过小说id查询
            return {"status_code": 0 ,"result":search_novel_by_novel_id(input)}
        case 2:#通过作者id查询
            return {"status_code": 0 ,"result":search_novel_by_writer_id(input)}
        case 3:#通过作者名查询
            return {"status_code": 0, "result":search_novel_by_writer_name(input)}
        case _:#返回状态为1，说明查询失败
            return {"status_code": 1 ,"result":[]}

@app.post("/apis/model/change", tags=["模型切换"],summary="用户向服务器发送模型切换请求")
async def change_model(model:str):
    message = "模型切换成功"
    return {message}

@app.post("/apis/write_request", tags=["AI写小说"],summary="用户向服务器发送AI写小说请求")
async def ai_write_novel(contents:Write_request ):
    contents = contents.contents
    response = ai01.call_with_messages(contents)
    return response

@app.post("/apis/answer_request", response_model=str , tags=["AI回答问题"],summary="用户向服务器发送让AI回答问题的请求")
async def ai_answer_question(question:Answer_request):
    question = question.question
    response = ai02.call_with_messages(question)
    return response

@app.get("/apis/items/get_user/{user_id}", response_model=str, tags=["获取用户信息"],summary="获取用户信息")
async def read_item(item_id: int, db: Session = Depends(get_db)):
    
    return "1111"

@app.get("/apis/items/get_user/all",  tags=["获取用户信息"],summary="获取所有用户信息")
    
    return "1111"

@app.get("/apis/items/get_user/all", response_model=schemas.Item, tags=["获取用户信息"],summary="获取所有用户信息")
async def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    
    return "123"

@app.delete("/apis/items/{item_id}", tags=["删除用户"],summary="删除用户信息")
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    
    return {"message": "Item deleted successfully"}


@app.get("/apis/novels/get/rank", tags=["获取小说信息"],summary="获取小说排行")
async def get_rank():
    message = "获取小说排行成功"
    return {message}

@app.post("/apis/novels/create", tags=["创建小说"],summary="数据库中插入小说")
async def create_novel(novel: int, db: Session = Depends(get_db)):
    return "小说创建成功"

@app.delete("/apis/novels/delete/{novel_id}", tags=["删除小说"],summary="删除小说")
def delete_novel(novel_id: int, db: Session = Depends(get_db)):
    
    return {"message": "Novel deleted successfully"}

@app.post("/apis/novels/update/views", tags=["更新小说"],summary="更新小说浏览量")
def update_novel_views(novel_id: int, db: Session = Depends(get_db)):
    return {"message": "Novel views updated successfully"}

@app.get("/apis/logs/login", tags=["获取日志"],summary="获取登录日志")
async def get_login_logs():
    message = "获取登录日志成功"
    return {message}

@app.get("/apis/logs/register", tags=["获取日志"],summary="获取注册日志")
async def get_register_logs():
    message = "获取注册日志成功"
    return {message}

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

@app.post("/admin/changepwd", tags=['超级用户权限'], summary='修改Admin密码',
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

@app.get("/admin/getNovel",tags=['超级用户权限'], summary='得到搜索目标或所有小说信息',
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

@app.get("/admin/getusers",tags=['超级用户权限'], summary='得到搜索目标或所有用户信息',
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

@app.delete("/admin/deleteuser",tags=['超级用户权限'], summary='删除用户', description="""
参数说明:\n
    --user_id:需要删除的用户id\n
    --user_name:需要删除的用户名\n
""")
async def admin_delete_user(user_id: int, user_name: str):
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

@app.delete("/admin/deletenovel", tags=['超级用户权限'], summary='删除小说', description="""
参数说明:\n
    --novel_id:需要删除的小说id\n
    --novel_title:需要删除的小说名\n
""")
async def admin_delete_novel(novel_id: int, novel_title: str):
    (s, msg) = db_method.delete_novel(novel_id, novel_title)
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

@app.post("/admin/resetpassword",tags=['超级用户权限'], summary='重置用户密码', description="""
参数说明:\n
    --user_id:用户id\n
    --user_name:用户名\n
""")
async def admin_reset_password(user_id: int, user_name: str):
    (s, m) = db_method.reset_password(user_id, user_name)
    if not s:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=m
        )
    return {'message': m}

@app.get("/admin/getusernovel", tags=['超级用户权限'], summary='查找某个用户发布的小说', description="""
参数说明:
    user_id:用户名
返回:小说""")
async def admin_get_user_novel(user_id: int):
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