from pydantic import BaseModel, ConfigDict, Json
from datetime import datetime, date
from typing import Optional
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.system.task import SchedulerTaskRecord


class TaskDTO(BaseModel):
    name: str = None
    group: Optional[str] = None
    job_class: str = None
    exec_strategy: str = None
    expression: str = None
    is_active: Optional[bool] = True
    remark: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


class TaskSimpleOutDTO(TaskDTO):
    id: int
    create_datetime: Optional[datetime] = None
    update_datetime: Optional[datetime] = None
    last_run_datetime: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


SchedulerTaskRecordDTO = pydantic_model_creator(
    SchedulerTaskRecord, name=f"{SchedulerTaskRecord.__name__}DTO"
)
