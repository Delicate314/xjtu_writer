from fastapi import Depends, FastAPI, HTTPException, UploadFile, status, Query, Form, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from . import schemas, ai01, ai02, login_and_rigister, models
from pydantic import BaseModel
import os, shutil
import urllib.parse
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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



@app.post("/apis/register",tags=["用户注册"],summary="用户注册")
async def register(user_register: models.UserRegister):
    message = login_and_rigister.register(user_register)
    return message

@app.post("/apis/login", tags=["用户登录"],summary="用户向服务器发送登录请求")
async def login(user_login: models.UserLogin):
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

