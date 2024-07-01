
import datetime
import asyncio
import pytz
import json
from apscheduler.events import EVENT_JOB_EXECUTED, JobExecutionEvent
from tortoise.exceptions import DoesNotExist, IntegrityError
from app.models.system.task import SchedulerTask, SchedulerTaskRecord

def before_job_execution(event: JobExecutionEvent):
    asyncio.create_task(async_before_job_execution(event))


async def async_before_job_execution(event: JobExecutionEvent):
    timezone = pytz.timezone("Asia/Shanghai")
    start_time: datetime.datetime = event.scheduled_run_time.astimezone(timezone)
    end_time = datetime.datetime.now(timezone)
    process_time = (end_time - start_time).total_seconds()

    # # Ensure both are aware or naive (in this case, making both aware)
    # if start_time.tzinfo is None:
    #     start_time = timezone.localize(start_time)

    process_time = (end_time - start_time).total_seconds()
    job_id = event.job_id.split("-")[0]

    result = {
        "job_id": event.job_id,
        "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
        "process_time": process_time,
        "retval": json.dumps(event.retval),
        "exception": json.dumps(event.exception),
        "traceback": json.dumps(event.traceback),
    }

    try:
        task = await SchedulerTask.get(id=job_id)
        result.update(
            {
                "job_class": task.job_class,
                "name": task.name,
                "group": task.group,
                "exec_strategy": task.exec_strategy,
                "expression": task.expression,
            }
        )
    except DoesNotExist:
        result["exception"] = f"Task with id {job_id} does not exist"
    except Exception as e:
        result["exception"] = f"Task Query Exception: {e}"

    await SchedulerTaskRecord.create(**result)
