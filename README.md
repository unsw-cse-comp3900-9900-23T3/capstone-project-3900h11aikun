# Backend 进展

### 2023-11-08 再次更新了数据库，所有的qualification是 master， undergraduate， doctorate 三选一。所有的skill （student 的，和supervisor的） 都是从 `['Java', 'Pthon', 'Javascript', 'C/C++', 'Machine Learning', 'Deep Learning', 'Software Develop', 'Networking', 'Database/Big Data']` 这里面进行挑选。数据库是这样的的design，每个学生和supervisor随机匹配了9个skill里面的6个，然后每个project是随机匹配了9个skill里面的4个。这样就是确保recommendation可以working。

### 注意每个skills 是个string， 用 逗号+空格 的形式隔开！！！。 逗号+空格！！比如说 `Machine Learning, Java, Deep Learning, Pthon, Networking, Javascript` 这样的。

### 同时check了一下 recommend 的api。 如果最后的res 是长度为0，那么从所有的project里面随机选两个project。这样保证recommendation是能return些东西的。

### 还有一点，project 的status， 数据库的设计是 `"is_open", "in_progress", "is_closed"` 三选一，我把project update 和 post new project 的地方重新做了一下input data 的validation。

### 最后，每个database里面已经有的project，如果有progress，我都link到了一份uploads 里面的文件。

### 最后，uploads文件夹回归。


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
