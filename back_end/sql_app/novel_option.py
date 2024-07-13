import pymysql
from fastapi import HTTPException, UploadFile, Form, File
import os, shutil
from pydantic import BaseModel
import urllib.parse
from fastapi.responses import FileResponse, JSONResponse

from .search_novel import *
from .connect_sql import *

class Novel(BaseModel):
    novel_id: str

class SearchNovel(BaseModel):
    func: str
    input: str

class GetNovel(BaseModel):
    novel_id: int
    page: int = 1
    page_size: int = 10

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
    
DIR = "/home/xjtu_writer/xjtu_writer/novel"

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

async def import_file(
    file: UploadFile = File(...),
    user_id: str = Form(...)
):
    # 判断文件类型，只支持txt文件
    if file.content_type != "text/plain":
        raise HTTPException(status_code=400, detail="Invalid file type. Only .txt files are allowed.")
    # 检查文件扩展名
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Invalid file extension. Only .txt files are allowed.")
    
    # 读取文件内容并转换为字符串
    file_content = await file.read()
    file_text = file_content.decode('utf-8')
    
    return {"user_id": user_id, "novel": file_text}

async def download_file(input: Novel):
    novel_id = input.novel_id
    #try:
    # 获取小说信息
    novel_info = search_novel_by_novel_id(novel_id)
    if len(novel_info) == 0:
        raise HTTPException(status_code=404, detail="File not found")
        
    # 获取作者id用来构造文件路径
    writer_id = novel_info[0]['user_id']
    # 获取小说名用来构造文件名
    novel_title = novel_info[0]['novel_title']
    #except Exception as e:
        #raise HTTPException(status_code=500, detail=str(e))

    file_path = os.path.join(DIR, str(writer_id), f"{novel_id}.txt")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    response = FileResponse(file_path, media_type='text/plain')
    # 设置文件下载时的文件名，确保支持中文文件名
    response.headers["Content-Disposition"] = f"attachment; filename*=UTF-8''{urllib.parse.quote(novel_title)}.txt"

    return response


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

async def view_count_add_one(novel_id: str):
    sql_select = "SELECT novel_viewcount FROM novel_info WHERE novel_id = %s"
    sql_update = "UPDATE novel_info SET novel_viewcount = novel_viewcount + 1 WHERE novel_id = %s"
    
    db = get_db()
    try:
        cursor = db.cursor()
        
        # 查询小说是否存在
        cursor.execute(sql_select, (novel_id,))
        result = cursor.fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="Novel not found")
        
        # 更新 view_count
        cursor.execute(sql_update, (novel_id,))
        db.commit()
        
        # 获取新的 view_count
        new_view_count = result[0] + 1
    except pymysql.Error as err:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {err}")
    finally:
        cursor.close()
        db.close()
    
    return {"novel_id": novel_id, "new_view_count": new_view_count}
        
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
    await view_count_add_one(novel_id)
    return JSONResponse(response)


def delete_novel(novel_id: int, novel_name: str):
    cursor = None
    try:
        result = search_novel_by_novel_id(str(novel_id))
        if not result:
            return (0, '小说文件未找到或不存在')
        
        user_id = result[0]["user_id"]
        db = get_db()
        cursor = get_cursor(db)
        
        # 执行删除操作
        delete_sql = "DELETE FROM novel_info WHERE novel_id = %s AND novel_title = %s"
        cursor.execute(delete_sql, (novel_id, novel_name))
        
        # 检查是否成功删除
        if cursor.rowcount == 0:
            return (0, '小说记录未找到或不存在')
        
        # 提交事务
        cursor.connection.commit()

        # 生成文件路径
        user_dir = os.path.join(DIR, str(user_id))
        file_path = os.path.join(user_dir, f"{novel_id}.txt")
        
        # 删除文件
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            return (1, "文件未找到")
    except Exception as e:
        if cursor:
            cursor.connection.rollback()  # 回滚事务
        return (1, f"An error occurred while deleting the novel: {str(e)}")
    
    finally:
        if cursor:
            cursor.close()  # 确保关闭游标
        db.close()
    
    return (2, "小说删除成功")


async def release_novel(novel: str, user_id: str, novel_title : str):
    # 创建用户目录，如果不存在的话
    user_dir = os.path.join(DIR, user_id)
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)

    # 将小说插入数据库，并获取小说id
    novel_id = insert_novel_to_sql(user_id=user_id, novel_title=novel_title, novel_path=user_dir)
    if novel_id is None:
        raise HTTPException(status_code=400, detail="Insert failed, the novel id is none")

    # 生成文件路径
    file_path = os.path.join(user_dir, f"{novel_id}.txt")

    # 保存小说内容到文件
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(novel)

    return {"file_path": file_path, "novel_id": novel_id}