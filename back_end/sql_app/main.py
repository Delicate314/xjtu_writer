from fastapi import Depends, FastAPI, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from . import crud, schemas, ai01, ai02, login_and_rigister, models
from .database import SessionLocal, engine




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
async def login(user_register: models.UserRegister):
    message = login_and_rigister.register(user_register)
    return message

@app.post("/apis/login", tags=["用户登录"],summary="用户向服务器发送登录请求")
async def login(user_login: models.UserLogin):
    message = login_and_rigister.login(user_login)
    return message

@app.post("/apis/model/change", tags=["模型切换"],summary="用户向服务器发送模型切换请求")
async def change_model(model:str):
    message = "模型切换成功"
    return {message}

@app.post("/apis/write_request", tags=["AI写小说"],summary="用户向服务器发送AI写小说请求")
async def ai_write_novel(contents:str ):
    response = ai01.call_with_messages(contents)
    return response

@app.post("/apis/answer_request", response_model=str , tags=["AI回答问题"],summary="用户向服务器发送让AI回答问题的请求")
async def ai_answer_question(question:str):
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

@app.get("/apis/novels/get",  tags=["获取小说信息"],summary="获取小说")
async def read_novel(novel_id: int, db: Session = Depends(get_db)):
    
    return "123"

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

