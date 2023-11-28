import sqlite3

class DataManager:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.create_tables()

    def create_tables(self):
        # 在数据库中创建必要的表
        with self.connection:
            self.connection.execute(
                '''CREATE TABLE IF NOT EXISTS ac_usage (
                    id INTEGER PRIMARY KEY,
                    room_number TEXT NOT NULL,
                    temperature INTEGER,
                    wind_speed INTEGER,
                    start_time TEXT,
                    end_time TEXT
                )'''
            )

    def record_usage(self, room_number, temperature, wind_speed, start_time, end_time):
        # 记录空调的使用情况
        with self.connection:
            self.connection.execute(
                '''INSERT INTO ac_usage (room_number, temperature, wind_speed, start_time, end_time) 
                   VALUES (?, ?, ?, ?, ?)''',
                (room_number, temperature, wind_speed, start_time, end_time)
            )

    def fetch_records(self):
        # 获取所有使用记录
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM ac_usage")
            return cursor.fetchall()

    # 可以根据需要添加更多与数据管理相关的方法
