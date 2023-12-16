# 项目介绍
  
# 环境依赖
    flask == 3.0.0
    Python >= 3.8
    Werkzeug >= 3.0.0   

# 目录结构介绍
```
backend/
|-- app/
|      |--  static/          # 静态文件
|      |-- templates/       # 模板文件
|      |-- views/           # 视图函数
|          |-- auth.py       # 包含登录和注销的视图函数  
|          |-- data.py       # 包含数据收集相关的视图函数，弃用
|          |-- admin.py      # 包含设备管理相关的视图函数
|          |-- control.py    # 处理客户端控制操作
|          |-- client.py     # 处理有关客户端
|          |-- billing.py    # 生成账单和详单的视图函数
|          |-- query.py      # 包含数据查询相关的视图函数
|          |-- room.py       # 包含房间相关的视图函数
|      |-- config.py         # 配置文件
|      |-- run.py           # 构建实例
|      |-- models.py        # 数据库模型
|      |-- utils.py         # 存储辅助函数和工具函数
|-- data/
|      |-- Bupt.db          # sqlite数据库
|-- migrations/         # 数据库迁移文件
|-- tests/              # 测试文件
|-- cli.py          # 运行文件
|-- README.MD        
```

**调度基本完成，部分函数需要修改**

# 使用
```
flask run --host=0.0.0.0 --port=11451 --debug   # 运行项目

# 初始化数据库
set FLASK_APP=cli.py
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 问题
1. 不知道为什么在client.py和control.py中的字典不起作用
2. 在调度更新的时候缺少记录更新