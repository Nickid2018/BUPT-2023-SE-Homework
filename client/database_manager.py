import sqlite3
import os

class DatabaseManager:
    def __init__(self):
        self.db_file = 'ac_control.db'
        self.connect_db()

    def connect_db(self):
        """ 连接到SQLite数据库，如果数据库不存在，则创建它 """
        self.conn = sqlite3.connect(self.db_file)
        self.create_table()

    def create_table(self):
        """ 创建一个表格来存储空调状态信息 """
        create_table_sql = '''
            CREATE TABLE IF NOT EXISTS ac_states (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_id TEXT NOT NULL,
                mode TEXT,
                temperature TEXT,
                wind_speed TEXT,
                sweep BOOLEAN,
                start_time TEXT,
                end_time TEXT,
                duration INTEGER
            );
        '''
        self.conn.execute(create_table_sql)
        self.conn.commit()

    def log_state(self, state):
        """ 记录空调的当前状态 """
        with self.conn:
            self.conn.execute('''
                INSERT INTO ac_states (room_id, mode, temperature, wind_speed, sweep, start_time, end_time, duration)
                VALUES (:room_id, :mode, :temperature, :wind_speed, :sweep, :start_time, :end_time, :duration)
            ''', {
                'room_id': state.get('room_id'),
                'mode': state.get('mode'),
                'temperature': state.get('temperature'),
                'wind_speed': state.get('wind_speed'),
                'sweep': state.get('sweep'),
                'start_time': state.get('start_time'),
                'end_time': state.get('end_time'),
                'duration': state.get('duration')
            })

    def close(self):
        """ 关闭数据库连接 """
        self.conn.close()
