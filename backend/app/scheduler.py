from collections import deque
from datetime import datetime, timedelta
from app import db
import time
import asyncio

from app.models import Device, Status
from sqlalchemy import desc
from app.utils import generate_timestamp_id


def scheduler_operation(room_number_id, operation):
    selected_room = room_scheduler_map[room_number_id]

    # 查询最新状态
    status = (
        Status.query.filter_by(room_id=room_number_id)
        .order_by(desc(Status.last_update))
        .first()
    )

    # 生成随机id
    status_id = generate_timestamp_id()

    new_status = Status(
        id=status_id,
        room_id=status.room_id,
        temperature=status.temperature,
        wind_speed=status.wind_speed,
        mode=status.mode,
        sweep=status.sweep,
        is_on=status.is_on,
        last_update=datetime.utcnow(),
    )

    # 根据操作类型执行相应的操作
    if operation == "start":
        new_status.is_on = True
    else:
        new_status.is_on = False

    # 提交到数据库
    db.session.add(new_status)
    db.session.commit()


class RoomScheduler:
    def __init__(self, room_id, initial_temperature, target_temperature):
        self.room_id = room_id
        self.priority = 0  # 默认设为0
        self.current_temperature = initial_temperature
        self.initial_temperature = initial_temperature
        self.target_temperature = target_temperature
        self.is_on = False  # 房间初始时空调是关闭的
        self.last_scheduler_time = time.time()  # 最后被调度时间，配合调度算法
        self.mode = "cool"  # 默认模式是制冷
        self.last_update_temperature = time.time()  # 最后更新温度的时间，配合房间温度算法

    def update_temperature(self):
        current_time = time.time()
        time_elapsed = current_time - self.last_update_temperature

        if self.is_on:
            time_increment = int(time_elapsed / 10)  # 向下取整到最近的10秒的倍数
            if self.mode == "cool":
                if self.current_temperature >= self.target_temperature:
                    change_temperature = self.current_temperature - 0.5 * time_increment
                    self.current_temperature = max(
                        change_temperature, self.target_temperature
                    )
                    self.last_update_temperature += time_increment * 10
                else:
                    self.current_temperature = self.target_temperature
            else:
                if self.current_temperature <= self.target_temperature:
                    change_temperature = self.current_temperature + 0.5 * time_increment
                    self.current_temperature = min(
                        change_temperature, self.target_temperature
                    )
                    self.last_update_temperature += time_increment * 10
                else:
                    self.current_temperature = self.target_temperature
        else:  # 这里只写了在夏天的逻辑
            time_increment = int(time_elapsed / 10)  # 向下取整到最近的10秒的倍数
            if self.current_temperature <= self.initial_temperature:
                change_temperature = self.current_temperature + 0.5 * time_increment
                self.current_temperature = min(
                    change_temperature, self.initial_temperature
                )
                self.last_update_temperature += time_increment * 10


class Scheduler:
    def __init__(self):
        self.waiting_queue = deque()  # 等待队列
        self.service_queue = deque()  # 服务队列

    def add_room_queue(self, room):
        current_time = time.time()
        if len(self.service_queue) < 3 and len(self.waiting_queue) == 0:
            self.service_queue.append(room)
            room.last_scheduled_time = current_time
            return 1  # 代表成功开启服务
        else:
            self.waiting_queue.append(room)
            return 0  # 代表进入等待队列

    def close_air_conditioner(self, room):
        # 关闭空调，将房间从服务队列或等待队列中移除
        current_time = time.time()
        room.is_on = False
        if room in self.service_queue:
            self.service_queue.remove(room)
            room.last_update_temperature = current_time
        if room in self.waiting_queue:
            self.waiting_queue.remove(room)

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
            room.is_on = False
            room.update_temperature()
            room.last_update_temperature = current_time

            # 更新数据库记录
            room_id = room.id
            operation = "stop"
            scheduler_operation(room_id, operation)

            self.waiting_queue.append(room)

        # 将等待队列的对象进行调度
        while self.waiting_queue and len(self.service_queue) < 3:
            room = self.waiting_queue.popleft()
            room.last_scheduled_time = current_time
            room.is_on = True
            room.update_temperature()
            room.last_update_temperature = current_time

            # 更新数据库记录
            room_id = room.id
            operation = "start"
            scheduler_operation(room_id, operation)

            self.service_queue.append(room)

    def run_scheduler(self):
        while True:
            self.schedule_rooms()
            asyncio.sleep(10)  # 每10秒执行一次调度


# 实例化调度器
scheduler = Scheduler()

room_scheduler_map = {}
