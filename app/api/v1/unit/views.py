'''
Descripttion: 
version: 0.x
Author: zhai
Date: 2024-06-03 21:44:30
LastEditors: zhai
LastEditTime: 2024-06-03 21:47:44
'''


from fastapi import Depends

from app.utils.crud.tortoise_crud import TortoiseCRUDRouter
from app.utils.crud._types import UserDataOption
from app.utils.crud._utils import resp_success
from app.api.v1.unit.schema import UnitCreateDTO, UnitDTO
from app.models.ifd import UnitModel
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

router = TortoiseCRUDRouter(
    schema=UnitDTO,
    create_schema=UnitCreateDTO,
    db_model=UnitModel,
    prefix="unit"
)



@router.post("/custom_router")
async def test(
    para1: int,
    para2: str
):
    return resp_success(data="test custom router")


# @dummy_router.get('')
# def overloaded_get_all():
#     return 'My overloaded route that returns all the items'

# @dummy_router.get('/{item_id}')
# def overloaded_get_one():
#     return 'My overloaded route that returns one item'

