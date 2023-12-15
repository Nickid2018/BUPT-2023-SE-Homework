from collections import deque
from datetime import datetime, timedelta
from app import db
import time


class RoomScheduler:
    def __init__(self, room_id, initial_temperature, target_temperature):
        self.room_id = room_id
        self.priority = 0  # 默认设为0
        self.current_temperature = initial_temperature
        self.initial_temperature = initial_temperature
        self.target_temperature = target_temperature
        self.is_on = False  # 房间初始时空调是关闭的
        self.last_scheduler_time = time.time()  # 最后被调度时间，配合调度算法
        self.last_update_temperature = time.time()  # 最后更新温度的时间，配合房间温度算法


class Scheduler:
    def __init__(self):
        self.waiting_queue = deque()  # 等待队列
        self.service_queue = deque()  # 服务队列

    def add_room_waiting_queue(self, room):
        self.waiting_queue.append(room)

    def schedule_rooms(self):
        # 优先级调度
        self.waiting_queue = deque(
            sorted(self.waiting_queue, key=lambda r: r.priority, reverse=True)
        )

        # 时间片调度
        current_time = time.time()
        while (
            self.service_queue
            and (current_time - self.service_queue[0].last_scheduled_time) >= 20
        ):
            room = self.service_queue.popleft()
            room.last_scheduled_time = current_time
            self.waiting_queue.append(room)

    def run_scheduler(self):
        while True:
            self.schedule_rooms()
            time.sleep(10)  # 每10秒执行一次进度


# 房间初始化
room1 = RoomScheduler(room_id=1, initial_temperature=32, target_temperature=25)
room2 = RoomScheduler(room_id=2, initial_temperature=28, target_temperature=25)
room3 = RoomScheduler(room_id=3, initial_temperature=30, target_temperature=25)
room4 = RoomScheduler(room_id=4, initial_temperature=29, target_temperature=25)
room5 = RoomScheduler(room_id=5, initial_temperature=35, target_temperature=25)
