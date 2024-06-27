from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException, Query, Depends, Request
from tortoise.expressions import Q

from app.api.v1.task.schema import TaskDTO, TaskSimpleOutDTO
from app.controllers import user_controller
from app.controllers.log import log_controller
from app.core.crud import Total
from app.core.ctx import CTX_USER_ID
from app.models.system import User, Role, Log, APILog
from app.models.system import LogType
from app.models.system.task import SchedulerTask, SchedulerTaskRecord
from app.schemas.base import Success, SuccessExtra, Fail
from app.schemas.logs import LogUpdate, LogSearch
from apscheduler.jobstores.base import ConflictingIdError

router = APIRouter()

# , response_model=List[TaskSimpleOut]
@router.get("/tasks", summary="获取定时任务列表")
async def get_tasks(
     page: int = Query(1, description="页码"),
        page_size: int = Query(10, description="每页数量"),
        name:str= Query(None, description="name"),
        job_id:str= Query(None, description="id"),
        group:str= Query(None, description="分组"),
        # v_order:str= Query("desc", description="排序"),
):
    search = Q()

    if name:
        search &= Q(name__icontains=("like", name))
    if job_id:
        search &= Q(job_id__icontains=("like", job_id))
    if group:
        search &= Q(group=group)

    query = SchedulerTask.filter(search)
    total = await query.count()
    result = await query.offset((page - 1) * page_size).limit(page_size)
    # .order_by(*order)
    return SuccessExtra(data=result, total=total, current=page, size=page_size)

    # tasks = await SchedulerTask.filter(query).limit(p.params.limit).offset(p.params.offset).order_by("-create_datetime")
    # return [TaskSimpleOut(**task.__dict__) for task in tasks]


# class Task(BaseModel):
#     name: str
#     group: Optional[str] = None
#     job_class: str
#     exec_strategy: str
#     expression: str
#     is_active: Optional[bool] = True
#     remark: Optional[str] = None
#     start_date: Optional[datetime] = None
#     end_date: Optional[datetime] = None

# exec_strategy = data.get("exec_strategy")
# job_params = {
#     "name": data.get("_id"),
#     "job_class": data.get("job_class"),
#     "expression": data.get("expression")
# }
# if exec_strategy == "interval" or exec_strategy == "cron":
#     job_params["start_date"] = data.get("start_date")
#     job_params["end_date"] = data.get("end_date")
# message = {
#     "operation": self.JobOperation.add.value,
#     "task": {
#         "exec_strategy": data.get("exec_strategy"),
#         "job_params": job_params
#     }
# }

@router.post("/tasks", summary="添加定时任务")
async def post_tasks(request: Request, data: TaskDTO):


    exec_strategy = data.exec_strategy
    job_params = {
        "name": data.name,
        "job_class": data.job_class,
        "expression": data.expression
    }
    if exec_strategy == "interval" or exec_strategy == "cron":
        job_params["start_date"] = data.start_date
        job_params["end_date"] = data.end_date

    
    scheduler = request.app.state.task
    ret = scheduler.add_job(exec_strategy, job_params)
    if ret:
        return {"msg": "任务添加成功"}
    else:
        return {"msg": "报错"}
    



@router.put("/tasks", summary="更新定时任务")
async def put_tasks(request: Request, _id: int, data: TaskDTO):
    task = await SchedulerTask.get(id=_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    await task.update_from_dict(data.dict(exclude_unset=True)).save()
    scheduler = request.app.state.task
    scheduler.remove_job(str(_id))
    trigger = scheduler.__get_trigger_from_expression(data.exec_strategy, data.expression)
    scheduler.add_job(data.job_class, trigger, str(_id), args=(), kwargs={})
    return {"msg": "任务更新成功"}


@router.delete("/tasks", summary="删除单个定时任务")
async def delete_task(request: Request, _id: int):
    task = await SchedulerTask.get(id=_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    await task.delete()
    scheduler = request.app.state.task
    scheduler.remove_job(str(_id))
    return {"msg": "任务删除成功"}


@router.get("/task", summary="获取定时任务详情", response_model=TaskSimpleOutDTO)
async def get_task(request: Request, _id: int):
    task = await SchedulerTask.get(id=_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    return TaskSimpleOutDTO(**task.__dict__)


@router.post("/task", summary="执行一次定时任务")
async def run_once_task(request: Request, _id: int):
    task = await SchedulerTask.get(id=_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    scheduler = request.app.state.task

    exec_strategy = "once"
    job_params = {
                "name": task.get("id"),
                "job_class": task.get("job_class")
            }
    ret = scheduler.add_job(exec_strategy, job_params)
    if ret:
        return {"msg": "任务已执行"}
    else:
        return {"msg": "报错"}


@router.get("/task/group/options", summary="获取定时任务分组选择项列表")
async def get_task_group_options():
    groups = await SchedulerTask.all().values_list('group', flat=True).distinct()
    return groups


@router.get("/task/records", summary="获取定时任务调度日志列表")
async def get_task_records(request: Request, 
                             page: int = Query(1, description="页码"),
        page_size: int = Query(10, description="每页数量"),
        name:str= Query(None, description="name"),
        job_id:str= Query(None, description="id"),
          ):
    search = Q()

    if name:
        search &= Q(name__icontains=("like", name))
    if job_id:
        search &= Q(job_id__icontains=("like", job_id))
   

    query = SchedulerTaskRecord.filter(search)
    total = await query.count()
    result = await query.offset((page - 1) * page_size).limit(page_size).order_by("-create_datetime")
    # .order_by(*order)
    return Total(total), result



