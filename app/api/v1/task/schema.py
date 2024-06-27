from pydantic import BaseModel, ConfigDict, Json
from datetime import datetime, date
from typing import Optional


class TaskDTO(BaseModel):
    name: str
    group: Optional[str] = None
    job_class: str
    exec_strategy: str
    expression: str
    is_active: Optional[bool] = True
    remark: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class TaskSimpleOutDTO(TaskDTO):
    id: int
    create_datetime: datetime
    update_datetime: datetime
    last_run_datetime: Optional[datetime] = None
