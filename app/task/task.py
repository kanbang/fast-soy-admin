
import datetime
from enum import Enum
import random
from apscheduler.jobstores.base import ConflictingIdError

from app.models.system.task import SchedulerTask, SchedulerTaskRecord
from .scheduler import Scheduler
from loguru import logger


class ScheduledTask:

    class JobExecStrategy(Enum):
        interval = "interval"
        date = "date"
        cron = "cron"
        once = "once"

    def __init__(self):
        self.scheduler = None

    def add_job(self, exec_strategy: str, job_params: dict) -> None:
        """
        添加定时任务
        :param exec_strategy: 执行策略
        :param job_params: 执行参数
        :return:
        """
        name = job_params.get("name", None)
        error_info = None
        try:
            if exec_strategy == self.JobExecStrategy.interval.value:
                self.scheduler.add_interval_job(**job_params)
            elif exec_strategy == self.JobExecStrategy.cron.value:
                self.scheduler.add_cron_job(**job_params)
            elif exec_strategy == self.JobExecStrategy.date.value:
                self.scheduler.add_date_job(**job_params)
            elif exec_strategy == self.JobExecStrategy.once.value:
                # 这种方式会自动执行事件监听器，用于保存执行任务完成后的日志
                job_params["name"] = f"{name}-temp-{random.randint(1000, 9999)}"
                self.scheduler.add_date_job(**job_params, expression=datetime.datetime.now())
            else:
                raise ValueError("无效的触发器")
        except ConflictingIdError as e:
            # 任务编号已存在，重复添加报错
            error_info = "任务编号已存在"
        except ValueError as e:
            error_info = e.__str__()

        if error_info:
            logger.error(f"任务编号：{name}，报错：{error_info}")
            self.error_record(name, error_info)
            return False
        return True

    
    async def error_record(self, name: str, error_info: str) -> None:
        """
        添加任务失败记录，并且将任务状态改为 False
        :param name: 任务编号
        :param error_info: 报错信息
        :return:
        """
        try:
            task = await SchedulerTask.get(name=name)
            task.is_active = False
            await task.save()

            result = {
                "job_id": name,
                "job_class": task.job_class,
                "name": task.name,
                "group": task.group,
                "exec_strategy": task.exec_strategy,
                "expression": task.expression,
                "start_time": datetime.datetime.now(),
                "end_time": datetime.datetime.now(),
                "process_time": 0,
                "retval": "任务添加失败",
                "exception": error_info,
                "traceback": None
            }
            await SchedulerTaskRecord.create(**result)
        except ValueError as e:
            logger.error(f"任务编号：{name}, 报错：{e}")

    def run(self) -> None:
        """
        启动定时任务
        :return:
        """
        self.scheduler = Scheduler()
        self.scheduler.start()
        print("Scheduler 启动成功")


    def close(self) -> None:
        """
        # pycharm 执行停止，该函数无法正常被执行，怀疑是因为阻塞导致或 pycharm 的强制退出导致
        # 报错导致得退出，会被执行
        关闭程序
        :return:
        """
        if self.scheduler:
            self.scheduler.shutdown()
      
