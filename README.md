# Backend 进展

现在后端已经有login和student register的接口了。后端的组员可以继续开发其他的接口。

## 数据库的话，请复制黏贴 backend/db/default_database.db 文件，黏贴到 backend 里面，就等于是和app.py, config.py 这些文件是同一个backend folder里面，同时重命名成database.db 

这样做的好处是，当大家在调试数据库的时候，不会影响我们的基础数据库，同时你调试的database.db 也不会被push到这个github仓库里面。

backend的运行方法： 
```
cd backend
确保你的terminal是在backend这个folder

pip install -r requirements.txt

如果是mac linux的话，
pip3 install -r requirements.txt

python app.py
或者mac或者linux的话
python3 app.py
```

后端是跑在 http://localhost:9998 端口。浏览器打开这个网址，可以看到后端接口的swagger doc。 

简单介绍一下文件：

**apis** 里面，每个不同的module分布在不同的apis 文件夹的py文件里面。记得在backend/config.py 里面做个import，详情请看backend/config.py

**db** folder里面是有个 model.py 文件，是数据库的每个table的定义。采用的是flask sqlalchemy 的object oriented 写法。每个table可以直接用这种class的形式来做数据库的CRUD操作。

**models** folder 里面是包含了每个request parser，或者body的parameter 定义。




