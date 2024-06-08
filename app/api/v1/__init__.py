'''
Descripttion: 
version: 0.x
Author: zhai
Date: 2024-05-31 21:27:14
LastEditors: zhai
LastEditTime: 2024-06-08 23:00:31
'''
from fastapi import APIRouter

from .auth import router_auth
from .route import router_route
from .system_manage import router_system_manage
from .dummy.views import router as dummy_router
from .unit.views import router as unit_router
from .mfs.views import mfs_router, mfst_router, equipment_router

v1_router = APIRouter()

v1_router.include_router(router_auth, prefix="/auth", tags=["权限认证"])
v1_router.include_router(router_route, prefix="/route", tags=["路由管理"])
v1_router.include_router(router_system_manage, prefix="/system-manage", tags=["系统管理"])
v1_router.include_router(dummy_router)
v1_router.include_router(unit_router)
v1_router.include_router(mfst_router)
v1_router.include_router(mfs_router)
v1_router.include_router(equipment_router)

