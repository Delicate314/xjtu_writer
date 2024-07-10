2024/7/10

search_novel：

修改了tuples_to_json
修改了search_novel_by_keyword、search_novel_by_novel_id、search_novel_by_writer_id的查询逻辑和返回值
增加了search_novel_by_writer_name，用来通过作者名查询


main:

修改了upload_file的存储逻辑，增加功能描述
修改了search_novel，增加通过作者名查询小说的功能，增加异常处理功能
增加了下载小说的功能
增加了获取小说的功能
修改了传参问题

前端代码示例（仅供参考）：

GetNovel：
将小说展示在终端

DownloadFile：
下载小说