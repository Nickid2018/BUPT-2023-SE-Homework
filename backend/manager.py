# 总管所有文件
from app import create_app, db
from flask_script import Manager
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)


if __name__ == '__main__':
    app.run()