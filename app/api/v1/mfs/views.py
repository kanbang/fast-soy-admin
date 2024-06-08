'''
Descripttion: 
version: 0.x
Author: zhai
Date: 2024-06-03 21:44:30
LastEditors: zhai
LastEditTime: 2024-06-08 22:59:38
'''


from fastapi import Depends

from app.api.v1.mfs.schema import EquipmentCreateDTO, EquipmentDTO, MfsCreateDTO, MfsDTO, MfstCreateDTO, MfstDTO
from app.models.ifd.plant import MFS, MFST, Equipment
from app.utils.crud.tortoise_crud import TortoiseCRUDRouter
from app.utils.crud._types import UserDataOption
from app.utils.crud._utils import resp_success
from app.api.v1.dummy.schema import DummyCreateDTO, DummyDTO
from app.models.dummy import DummyModel
from tortoise.contrib.pydantic import pydantic_model_creator


# Example query: [["age", ">=", "25"], ["name", "=", "Alice"]]


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# def token_auth(token: str = Depends(oauth2_scheme)):
#     print(token)
#     if not token:
#         raise HTTPException(401, "Invalid token")

# router = SQLAlchemyCRUDRouter(schema=DummyDTO, dependencies=[Depends(token_auth)])


# DummyDTO = pydantic_model_creator(DummyModel, name=f"{DummyModel.__name__}DTO")
# DummyCreateDTO = pydantic_model_creator(DummyModel, name=f"{DummyModel.__name__}CreateDTO", exclude_readonly=True)


mfst_router = TortoiseCRUDRouter(
    schema=MfstDTO,
    create_schema=MfstCreateDTO,
    db_model=MFST,
    prefix="mfst",
)

mfs_router = TortoiseCRUDRouter(
    schema=MfsDTO,
    create_schema=MfsCreateDTO,
    db_model=MFS,
    prefix="mfs",
)


equipment_router = TortoiseCRUDRouter(
    schema=EquipmentDTO,
    create_schema=EquipmentCreateDTO,
    db_model=Equipment,
    prefix="equipment",
)