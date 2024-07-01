from pydantic import (
    BaseModel,
    BeforeValidator,
    SerializerFunctionWrapHandler,
    ConfigDict,
    Field,
    Json,
    field_validator,
)
from datetime import datetime, date
from typing import Any, Dict, Optional
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.system.task import SchedulerTaskRecord

# 返回的时候可以转成时间戳，输入的时候会引起错误
# class TimestampBaseModel(BaseModel):
#     @field_validator('*')
#     def convert_datetimes_to_timestamps(cls, value: Any, field: Field) -> Any:
#         if isinstance(value, datetime):
#             return int(value.timestamp())
#         return value

from typing_extensions import Annotated
from pydantic.functional_serializers import WrapSerializer


def ser_wrap_datetime(v: datetime, nxt: SerializerFunctionWrapHandler) -> int:
    return int(v.timestamp() * 1000)


def datetime_stamp_js2py(v: any) -> any:
    if isinstance(v, (int, float)):
        return v / 1000
    return v


datetime_stamp = Annotated[
    datetime,
    BeforeValidator(datetime_stamp_js2py),
    WrapSerializer(ser_wrap_datetime, when_used="json"),
]


# class datetime_stamp(datetime):

# from pydantic.fields import FieldInfo
# class datetime_stamp(datetime):
#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate

#     @classmethod
#     def validate(cls, v: Any, field: FieldInfo) -> datetime:
#         if isinstance(v, (int, float)):
#             return datetime.fromtimestamp(v / 1000)
#         if isinstance(v, str):
#             return datetime.fromisoformat(v)
#         if isinstance(v, datetime):
#             return v
#         raise ValueError("Invalid value for datetime")

#     def __repr__(self) -> str:
#         return f"Timestamp({super().__repr__()})"

#     def __str__(self) -> str:
#         return str(int(self.timestamp() * 1000))

#     def __json__(self):
#         return int(self.timestamp() * 1000)


class TaskDTO(BaseModel):
    name: str = None
    group: Optional[str] = None
    job_class: str = None
    exec_strategy: str = None
    expression: str = None
    is_active: Optional[bool] = True
    remark: Optional[str] = None
    start_date: Optional[datetime_stamp] = None
    end_date: Optional[datetime_stamp] = None
    model_config = ConfigDict(from_attributes=True)


class TaskSimpleOutDTO(TaskDTO):
    id: int
    create_datetime: Optional[datetime_stamp] = None
    update_datetime: Optional[datetime_stamp] = None
    last_run_datetime: Optional[datetime_stamp] = None
    model_config = ConfigDict(from_attributes=True)


SchedulerTaskRecordDTO = pydantic_model_creator(
    SchedulerTaskRecord, name=f"{SchedulerTaskRecord.__name__}DTO"
)
