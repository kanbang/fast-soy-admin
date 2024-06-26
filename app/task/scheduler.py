from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, JobExecutionEvent

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.job import Job
from apscheduler.jobstores.base import ConflictingIdError, JobLookupError
from tortoise import Tortoise, fields, run_async
import datetime
import re

from app.task.listener import before_job_execution


DATABASE_URL = "sqlite:///scheduler.db"
# DATABASE_URL = "sqlite:///db_system.sqlite3"


class Scheduler:
    def __init__(self):
        self.scheduler = None

    def start(self, listener: bool = True) -> None:
        # self.scheduler = BackgroundScheduler()
        self.scheduler = AsyncIOScheduler()
        if listener:
            self.scheduler.add_listener(before_job_execution, EVENT_JOB_EXECUTED)
        self.scheduler.add_jobstore(self.__get_sqlalchemy_job_store())
        self.scheduler.start()

    def __get_sqlalchemy_job_store(self) -> SQLAlchemyJobStore:
        return SQLAlchemyJobStore(url=DATABASE_URL)

    def add_job(
        self,
        job_class: str,
        trigger: CronTrigger | DateTrigger | IntervalTrigger,
        job_id: str = None,
        *args,
        **kwargs,
    ) -> Job | None:
        job_class = self.__import_module(job_class)
        if job_class:
            return self.scheduler.add_job(
                job_class.main, trigger=trigger, args=args, kwargs=kwargs, id=job_id
            )
        else:
            raise ValueError(f"添加任务失败，未找到该模块下的方法：{job_class}")

    def add_cron_job(
        self,
        job_class: str,
        expression: str,
        start_date: str = None,
        end_date: str = None,
        timezone: str = "Asia/Shanghai",
        job_id: str = None,
        args: tuple = (),
        **kwargs,
    ) -> Job | None:
        second, minute, hour, day, month, day_of_week, year = (
            self.__parse_cron_expression(expression)
        )
        trigger = CronTrigger(
            second=second,
            minute=minute,
            hour=hour,
            day=day,
            month=month,
            day_of_week=day_of_week,
            year=year,
            start_date=start_date,
            end_date=end_date,
            timezone=timezone,
        )
        return self.add_job(job_class, trigger, job_id, *args, **kwargs)

    def add_date_job(
        self,
        job_class: str,
        expression: str,
        job_id: str = None,
        args: tuple = (),
        **kwargs,
    ) -> Job | None:
        trigger = DateTrigger(run_date=expression)
        return self.add_job(job_class, trigger, job_id, *args, **kwargs)

    def add_interval_job(
        self,
        job_class: str,
        expression: str,
        start_date: str | datetime.datetime = None,
        end_date: str | datetime.datetime = None,
        timezone: str = "Asia/Shanghai",
        jitter: int = None,
        job_id: str = None,
        args: tuple = (),
        **kwargs,
    ) -> Job | None:
        second, minute, hour, day, week = self.__parse_interval_expression(expression)
        trigger = IntervalTrigger(
            weeks=week,
            days=day,
            hours=hour,
            minutes=minute,
            seconds=second,
            start_date=start_date,
            end_date=end_date,
            timezone=timezone,
            jitter=jitter,
        )
        return self.add_job(job_class, trigger, job_id, *args, **kwargs)

    def run_job(self, job_class: str, args: tuple = (), **kwargs) -> None:
        job_class = self.__import_module(job_class)
        job_class.main(*args, **kwargs)

    def remove_job(self, job_id: str) -> bool:
        try:
            self.scheduler.remove_job(job_id)
        except JobLookupError as e:
            print(f"删除任务失败, 报错：{e}")
            return False
        return True

    def remove_all_jobs(self) -> bool:
        try:
            self.scheduler.remove_all_jobs()
        except JobLookupError as e:
            print(f"删除任务失败, 报错：{e}")
            return False
        return True

    def get_job_status(self, job_id: str) -> str:
        job = self.scheduler.get_job(job_id)
        if job is None:
            return "not found"
        elif job.next_run_time is None:
            return "paused"
        else:
            return "running"

    def pause(self, job_id: str) -> bool:
        job = self.scheduler.get_job(job_id)
        if job:
            job.pause()
            return True
        return False

    def resume(self, job_id: str) -> bool:
        job = self.scheduler.get_job(job_id)
        if job:
            job.resume()
            return True
        return False

    def get_job(self, job_id: str) -> Job:
        return self.scheduler.get_job(job_id)

    def has_job(self, job_id: str) -> bool:
        return bool(self.get_job(job_id))

    def get_jobs(self) -> list[Job]:
        return self.scheduler.get_jobs()

    def get_job_names(self) -> list[str]:
        jobs = self.scheduler.get_jobs()
        return [job.id for job in jobs]

    def __import_module(self, expression: str):
        module, args = self.__parse_string_to_class(expression)
        try:
            module_pag, module_class = module.rsplit(".", 1)
            pag = __import__(module_pag, fromlist=[module_class])
            return getattr(pag, module_class)(*args)
        except (ModuleNotFoundError, AttributeError, TypeError) as e:
            raise ValueError(f"模块导入错误：{e}")

    @staticmethod
    def __parse_cron_expression(expression: str) -> tuple:
        fields = expression.strip().split()
        if len(fields) not in (6, 7):
            raise ValueError("无效的 Cron 表达式")
        parsed_fields = [None if field in ("*", "?") else field for field in fields]
        if len(fields) == 6:
            parsed_fields.append(None)
        return tuple(parsed_fields)

    @staticmethod
    def __parse_interval_expression(expression: str) -> tuple:
        fields = expression.strip().split()
        if len(fields) != 5:
            raise ValueError("无效的 interval 表达式")
        parsed_fields = [int(field) if field != "*" else 0 for field in fields]
        return tuple(parsed_fields)

    @classmethod
    def __parse_string_to_class(cls, expression: str) -> tuple:
        pattern = r"([\w.]+)(?:\((.*)\))?"
        match = re.match(pattern, expression)
        if match:
            class_path = match.group(1)
            arguments = match.group(2)
            arguments = cls.__parse_arguments(arguments) if arguments else []
            return class_path, arguments
        return None, None

    @staticmethod
    def __parse_arguments(args_str) -> list:
        arguments = []
        for arg in re.findall(
            r'"([^"]*)"|(\d+\.\d+)|(\d+)|([Tt]rue|[Ff]alse)', args_str
        ):
            if arg[0]:
                arguments.append(arg[0])
            elif arg[1]:
                arguments.append(float(arg[1]))
            elif arg[2]:
                arguments.append(int(arg[2]))
            elif arg[3]:
                arguments.append(arg[3].lower() == "true")
        return arguments

    def shutdown(self) -> None:
        self.scheduler.shutdown()


async def main():
    # atexit.register(lambda: Scheduler().shutdown())
    await Tortoise.init(db_url=DATABASE_URL, modules={"models": ["__main__"]})
    await Tortoise.generate_schemas()
    scheduler = Scheduler()
    scheduler.start()
    scheduler.add_cron_job('test.Test("jet",1)', "0 0 * * * *")


if __name__ == "__main__":
    run_async(main())
