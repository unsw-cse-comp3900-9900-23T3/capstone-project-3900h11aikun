现在后端已经有login和student register的接口了。后端的组员可以继续开发其他的接口。
数据库的话，请复制黏贴 backend/db/default_database.db 文件，黏贴到 backend 里面，就等于是和app.py, config.py 这些文件是同一个backend folder里面，同时重命名成database.db 

这样做的好处是，当大家在调试数据库的时候，不会影响我们的基础数据库，同时你调试的database.db 也不会被push到这个github仓库里面。

backend的运行方法： 
```
cd backend
确保你的terminal是在backend这个folder

pip install requirements.txt

如果是mac linux的话，
pip3 install requirements.txt

python app.py
或者mac或者linux的话
python3 app.py
```
