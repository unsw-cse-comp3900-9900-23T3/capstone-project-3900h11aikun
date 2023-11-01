# Backend 进展

## 2023-11-01 更新了数据库， supervisor也有了 resume url

## 每个人，pull 过最新的master 之后，都要！！重新！！复制黏贴 backend/db/default_database.db 文件，黏贴到 backend 里面，就等于是和 app.py, config.py 这些文件是同一个backend folder里面，同时重命名成*database.db*

## 注意，每个人的uploads里面，有两个文件，resume-1.pdf， resume-2.pdf，这两个文件是新的数据库里面，已有的student和supervisor每个人都被assign的resume。同时，uploads文件夹做了gitignore任何额外的文件的设置，这样子的话，你自己在本地test这个uploads的功能，你上传的文件，不会被传到github上。（在最终的版本的database里面，我们可以引入更多的resume的文件之类的。对于这方面如果有需要欢迎和backend组员说）

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




