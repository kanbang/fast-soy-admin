from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException, Query, Depends, Request
from tortoise.expressions import Q

from app.api.v1.task.schema import SchedulerTaskRecordDTO, TaskDTO, TaskSimpleOutDTO
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
from apscheduler.jobstores.base import JobLookupError

from app.utils.crud._utils import resp_success, resp_fail
from app.utils.crud.tortoise_crud import convert_to_pydantic


router = APIRouter()


# , response_model=List[TaskSimpleOut]
@router.get("", summary="获取定时任务列表")
async def get_tasks(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    name: str = Query(None, description="name"),
    job_id: str = Query(None, description="id"),
    group: str = Query(None, description="分组"),
    # v_order:str= Query("desc", description="排序"),
):
    search = Q()

    if name:
        search &= Q(name__icontains=name)
    if job_id:
        search &= Q(job_id__icontains=job_id)
    if group:
        search &= Q(group=group)

    query = SchedulerTask.filter(search)
    total = await query.count()
    role_objs = await query.offset((page - 1) * page_size).limit(page_size)

    return resp_success(convert_to_pydantic(role_objs, TaskSimpleOutDTO), total=total)

    # data = {"records": [
    #     TaskSimpleOutDTO.model_validate(role_obj).model_dump() for role_obj in role_objs
    # ]}

    # # .order_by(*order)
    # return SuccessExtra(data=data, total=total, current=page, size=page_size)


@router.post("", summary="添加定时任务")
async def post_tasks(request: Request, data: TaskDTO):

    task = await SchedulerTask.create(**data.model_dump(exclude_unset=True))
    record = convert_to_pydantic(task, TaskSimpleOutDTO)

    exec_strategy = data.exec_strategy
    job_params = {
        "job_id": str(task.id),
        "job_class": data.job_class,
        "expression": data.expression,
    }
    if exec_strategy == "interval" or exec_strategy == "cron":
        job_params["start_date"] = data.start_date
        job_params["end_date"] = data.end_date

    if data.is_active:
        scheduler = request.app.state.task
        ret = scheduler.add_job(exec_strategy, job_params)
        if ret:
            return resp_success(record, msg="任务添加成功(active)")
        else:
            return resp_fail(msg="报错")

    return resp_success(record, msg="任务添加成功(not active)")


@router.put("", summary="更新定时任务")
async def put_tasks(request: Request, _id: int, data: TaskDTO):
    task = await SchedulerTask.get(id=_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    await task.update_from_dict(data.model_dump(exclude_unset=True)).save()
    record = convert_to_pydantic(task, TaskSimpleOutDTO)

    scheduler = request.app.state.task
    ret = scheduler.remove_job(str(_id))

    # 这里不做判断，可以重复remove
    # if not ret:
    #     return Fail(msg="任务删除报错")

    if task.is_active:
        exec_strategy = task.exec_strategy
        job_params = {
            "job_id": str(task.id),
            "job_class": task.job_class,
            "expression": task.expression,
        }
        if exec_strategy == "interval" or exec_strategy == "cron":
            job_params["start_date"] = task.start_date
            job_params["end_date"] = task.end_date

        ret = scheduler.add_job(exec_strategy, job_params)

        if ret:
            return resp_success(record, msg="任务更新成功(active)")

        else:
            return resp_fail(msg="任务启动报错")

    return resp_success(record, msg="任务更新成功(not active)")


@router.delete("", summary="删除单个定时任务")
async def delete_task(request: Request, _id: int):
    task = await SchedulerTask.get(id=_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    await task.delete()
    scheduler = request.app.state.task
    ret = scheduler.remove_job(str(_id))
    if ret:
        record = convert_to_pydantic(task, TaskSimpleOutDTO)
        return resp_success(record, msg="任务删除成功")
    else:
        return resp_fail(msg="任务删除报错")


@router.delete("/all", summary="删除所有定时任务")
async def delete_all_tasks(request: Request):
    await SchedulerTask.all().delete()

    scheduler = request.app.state.task
    scheduler.remove_all_jobs()
    return resp_success(msg="删除所有定时任务成功")


@router.get("/{_id}", summary="获取定时任务详情", response_model=TaskSimpleOutDTO)
async def get_task(request: Request, _id: int):
    task = await SchedulerTask.get(id=_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    record = convert_to_pydantic(task, TaskSimpleOutDTO)
    return resp_success(record)


@router.post("/run_once", summary="执行一次定时任务")
async def run_once_task(request: Request, _id: int):
    task = await SchedulerTask.get(id=_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    scheduler = request.app.state.task

    exec_strategy = "once"
    job_params = {"job_id": str(task.id), "job_class": task.job_class}
    ret = scheduler.add_job(exec_strategy, job_params)
    if ret:
        return resp_success(msg="任务已执行")
    else:
        return resp_fail(msg="报错")

@router.get("/status/{job_id}", summary="获取定时任务状态")
async def get_task_status(request: Request, job_id: str):
    scheduler = request.app.state.task
    status = scheduler.get_job_status(job_id)
    return resp_success(msg=status)

@router.post("/pause/{job_id}", summary="暂停定时任务")
async def pause_task(request: Request, job_id: str):
    scheduler = request.app.state.task
    try:
        scheduler.pause(job_id)
        return {"message": f"任务 {job_id} 已暂停"}
    except JobLookupError:
        raise HTTPException(status_code=404, detail=f"任务 {job_id} 未找到")

@router.post("/resume/{job_id}", summary="恢复定时任务")
async def resume_task(request: Request, job_id: str):
    scheduler = request.app.state.task
    try:
        scheduler.resume(job_id)
        return {"message": f"任务 {job_id} 已恢复"}
    except JobLookupError:
        raise HTTPException(status_code=404, detail=f"任务 {job_id} 未找到")
    

@router.get("/groups", summary="获取定时任务分组选择项列表")
async def get_task_group_options():
    groups = await SchedulerTask.all().distinct().values("group")
    return resp_success(data=[group["group"] for group in groups])


@router.get("/records", summary="获取定时任务调度日志列表")
async def get_task_records(
    request: Request,
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    name: str = Query(None, description="name"),
    job_id: str = Query(None, description="id"),
):
    search = Q()

    if name:
        search &= Q(name__icontains=name)
    if job_id:
        search &= Q(job_id__icontains=job_id)

    query = SchedulerTaskRecord.filter(search)
    total = await query.count()
    role_objs = (
        await query.offset((page - 1) * page_size)
        .limit(page_size)
        .order_by("-start_time")
    )

    records = convert_to_pydantic(role_objs, SchedulerTaskRecordDTO)
    return resp_success(records, total=total)
