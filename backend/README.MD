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
|-- manager.py          # 运行文件
|-- README.MD        
```
## 目前还不知道数据库是怎么写的，所以仅提供了后端结构和部分视图函数的示例
## 结构可能存在缺陷，任何人可以修改
## 已完成函数中有关数据库的处理都为假设