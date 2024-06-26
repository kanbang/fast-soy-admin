from datetime import datetime
from typing import Optional, Type, Any

from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse, ORJSONResponse
import orjson
from pydantic import create_model
from starlette import status

from ._types import T, PAGINATION, PYDANTIC_SCHEMA

class CustomORJSONResponse(JSONResponse):
    def render(self, content: any) -> bytes:
        # 自定义的序列化函数，用于将 datetime 转换为时间戳
        def default(obj):
            if isinstance(obj, datetime):
                return int(obj.timestamp())
            raise TypeError

        return orjson.dumps(content, default=default, option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY)

class AttrDict(dict):  # type: ignore
    def __init__(self, *args, **kwargs) -> None:  # type: ignore
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def get_pk_type(schema: Type[PYDANTIC_SCHEMA], pk_field: str) -> Any:
    try:
        return schema.model_fields[pk_field].annotation
    except KeyError:
        return int


def schema_factory(
    schema_cls: Type[T], pk_field_name: str = "id", name: str = "Create"
) -> Type[T]:
    """
    Is used to create a CreateSchema which does not contain pk
    """

    fields = {
        f_name: (f.annotation, ... if f.is_required() else None)
        for f_name, f in schema_cls.model_fields.items()
        if f_name != pk_field_name
    }

    name = schema_cls.__name__ + name
    schema: Type[T] = create_model(__model_name=name, **fields)  # type: ignore
    return schema


def create_query_validation_exception(field: str, msg: str) -> HTTPException:
    return HTTPException(
        422,
        detail={
            "detail": [
                {"loc": ["query", field], "msg": msg, "type": "type_error.integer"}
            ]
        },
    )


def pagination_factory(max_limit: Optional[int] = None) -> Any:
    """
    Created the pagination dependency to be used in the router
    """

    def pagination(skip: int = 0, limit: Optional[int] = max_limit) -> PAGINATION:
        if skip < 0:
            raise create_query_validation_exception(
                field="skip",
                msg="skip query parameter must be greater or equal to zero",
            )

        if limit is not None:
            if limit <= 0:
                raise create_query_validation_exception(
                    field="limit", msg="limit query parameter must be greater then zero"
                )

            elif max_limit and max_limit < limit:
                raise create_query_validation_exception(
                    field="limit",
                    msg=f"limit query parameter must be less then {max_limit}",
                )

        return {"skip": skip, "limit": limit}

    return Depends(pagination)



# total:number 总记录数

def resp_success(
    data=None,
    total: int=None,
    code="0000",
    msg="OK",
    http_code=status.HTTP_200_OK,
    headers={},
):
    success = True if code == "0000" else False

    rdata = {"data": data}
    if total is not None:
        rdata["meta"] = {"total": total}

    content = dict(
        code=code, msg=msg, data=rdata, success=success
    )

    return ORJSONResponse(status_code=http_code, content=content, headers=headers)


def resp_fail(
    data=None,
    total=None,
    code="4000",
    msg="Fail",
    http_code=status.HTTP_200_OK,
    headers={},
):
    success = True if code == "0000" else False

    rdata = {"data": data}
    if total is not None:
        rdata["meta"] = {"total": total}

    content = dict(
        code=code, msg=msg, data=rdata, success=success
    )

    return ORJSONResponse(status_code=http_code, content=content, headers=headers)