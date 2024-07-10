from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse
from fastapi import Query

DIR = "/home/xjtu_writer/xjtu_writer/novel"

class UpFile(BaseModel):
    file: UploadFile
    novel_title: str
    user_id: str

@app.post("/apis/uploadfile", tags = ["上传文件"], description="""
          用户上传文件\n
          只支持txt文件\n
          文件存储位置: DIR/user_id/novel_id.txt\n""")
async def upload_file(input : UpFile):
    file = input.file
    novel_title = input.novel_title
    user_id = input.user_id
    #判断文件类型，只支持txt文件
    if file.content_type != "text/plain":
        raise HTTPException(status_code=400, detail="Invalid file type. Only .txt files are allowed.")
    #检查文件扩展名
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Invalid file extension. Only .txt files are allowed.")
    
    # 创建用户目录，如果不存在的话
    user_dir = os.path.join(DIR, user_id)
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)

    #将文件插入数据库，并获取小说id
    novel_id = insert_novel_to_sql(user_id = user_id, novel_title = novel_title, novel_path = user_dir)
    if novel_id == None:
        raise HTTPException(status_code=400, detail="insert failed, the novel id is none")
    
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


@app.post("/apis/getNovel", tags=["获取小说内容"],
         description ="""获取小说内容展示在终端\n
         注意：目前只有小说id为18时才有数据\n
         可以自己上传文件测试\n
         输入为小说id、获取的页数、获取的页大小\n
         这里的页大小指的是行数""")
async def show_file(input: Novel, page: int = Query(1, ge=1), page_size: int = Query(10, ge=1)):
    novel_id = input.novel_id
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
        raise HTTPException(status_code=500, detail=str(e))

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
    try:
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))