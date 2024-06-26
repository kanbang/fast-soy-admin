from datetime import datetime
from typing import (
    Any,
    Callable,
    List,
    Literal,
    Tuple,
    Type,
    TypeVar,
    cast,
    Coroutine,
    Optional,
    Union,
)

from fastapi import Depends, HTTPException, Request, Query
from fastapi.responses import ORJSONResponse
from fastapi.types import IncEx
from pydantic import BaseModel

from ._base import CRUDGenerator, NOT_FOUND
from ._types import (
    DEPENDENCIES,
    PAGINATION,
    PYDANTIC_SCHEMA as SCHEMA,
    RespModelT,
    UserDataOption,
    UserDataFilter,
    UserDataFilterAll,
    UserDataFilterSelf,
    InvalidQueryException,
    IdNotExist,
)
from ._utils import get_pk_type, resp_success

from tortoise.models import Model
from tortoise.queryset import QuerySet
from tortoise import fields, transactions
from tortoise.expressions import Q

CALLABLE = Callable[..., Coroutine[Any, Any, Model]]
CALLABLE_LIST = Callable[..., Coroutine[Any, Any, List[Model]]]

###########################################################################################
# Define a generic type variable
ModelType = TypeVar("ModelType", bound=Model)
PydanticType = TypeVar("PydanticType", bound=BaseModel)


# def model_to_dict_no_relation(model):
#     return {
#         column.name: getattr(model, column.name) for column in model.__table__.columns
#     }


def model_to_dict_no_relation(model: Model):
    # Get the fields of the model that are not relations
    non_relation_fields = {
        field_name: getattr(model, field_name)
        for field_name, field in model._meta.fields_map.items()
        if not isinstance(
            field,
            (
                fields.relational.ForeignKeyFieldInstance,
                fields.relational.BackwardFKRelation,
                fields.relational.ManyToManyFieldInstance,
            ),
        )
    }
    return non_relation_fields


def model_to_dict_relation(model, seen=None):
    if seen is None:
        seen = set()

    if model in seen:
        return None

    seen.add(model)

    result = {}

    # if field_name in model_class._meta.fetch_fields and issubclass(field_type, PydanticModel):
    #         subclass_fetch_fields = _get_fetch_fields(
    #             field_type, field_type.model_config["orig_model"]
    #         )
    #         if subclass_fetch_fields:
    #             fetch_fields.extend([field_name + "__" + f for f in subclass_fetch_fields])
    #         else:
    #             fetch_fields.append(field_name)
    # return fetch_fields

    for field_name, field in model._meta.fields_map.items():
        if isinstance(field, fields.relational.ForeignKeyFieldInstance):
            # await model.fetch_related(field_name)
            related = getattr(model, field_name)
            if related:
                result[field_name] = model_to_dict_no_relation(related)
        elif isinstance(
            field,
            (
                fields.relational.BackwardFKRelation,
                fields.relational.ManyToManyFieldInstance,
            ),
        ):
            # await model.fetch_related(field_name)
            related = getattr(model, field_name)
            if related:
                result[field_name] = [
                    model_to_dict_no_relation(item) for item in related.related_objects
                ]

                result[f"{field_name}_refids"] = [
                    getattr(item, "id") for item in related.related_objects
                ]
        else:
            result[field_name] = getattr(model, field_name)

    return result

    # await page.fetch_related('book')
    # book = page.book

    for relationship in model.__mapper__.relationships:
        try:
            related_obj = getattr(model, relationship.key)
        except Exception as e:
            result[relationship.key] = None
            continue

        if related_obj is None:
            result[relationship.key] = None
        else:
            if relationship.uselist:
                result[relationship.key] = [
                    model_to_dict_relation(item, seen) for item in related_obj
                ]
            else:
                result[relationship.key] = model_to_dict_relation(related_obj, seen)

    return result


def convert_to_pydantic(
    data: Union[dict, ModelType, List[ModelType]],
    pydantic_model: Type[PydanticType],
    relationships: bool = False,
    mode: Literal['json', 'python'] | str = 'python',
) -> Union[PydanticType, List[PydanticType]]:
    if data is None:
        return None
    elif isinstance(data, dict):
        return pydantic_model.model_validate(data).model_dump(mode=mode)
    elif isinstance(data, list):
        return [
            convert_to_pydantic(item, pydantic_model, relationships, mode) for item in data
        ]
    elif isinstance(data, Model):
        if relationships:
            return pydantic_model.model_validate(
                model_to_dict_relation(data),
            ).model_dump(mode=mode)
        else:
            return pydantic_model.model_validate(
                model_to_dict_no_relation(data),
            ).model_dump(mode=mode)
    else:
        raise ValueError("Invalid input data type")


# Mapping of operators to SQL operators
operator_mapping = {
    "=": "",
    "!=": "__not",
    ">": "__gt",
    "<": "__lt",
    ">=": "__gte",
    "<=": "__lte",
    "like": "__contains",
    "in": "__in",
}


def parse_query(
    query: List[
        Tuple[str, str, Union[str, int, float, datetime, List[Union[str, int, float]]]]
    ],
    queryset: QuerySet,
) -> QuerySet:
    filter_conditions = Q()

    for condition in query:
        if len(condition) != 3:
            raise InvalidQueryException(
                "Each condition must have exactly 3 elements: field, operator, and value."
            )

        field, operator, value = condition

        if operator not in operator_mapping:
            raise InvalidQueryException(f"Invalid operator: {operator}")

        # Construct the field name with the appropriate operator suffix
        field_with_operator = f"{field}{operator_mapping[operator]}"

        # Add the condition to the Q object
        filter_conditions &= Q(**{field_with_operator: value})

    return queryset.filter(filter_conditions)


class TortoiseCRUDRouter(CRUDGenerator[SCHEMA]):
    def __init__(
        self,
        schema: Type[SCHEMA],
        db_model: Type[Model],
        create_schema: Optional[Type[SCHEMA]] = None,
        update_schema: Optional[Type[SCHEMA]] = None,
        filter_schema: Optional[Type[SCHEMA]] = None,
        user_data_option: UserDataOption = UserDataOption.ALL_ONLY,
        prefix: Optional[str] = None,
        tags: Optional[List[str]] = None,
        paginate: Optional[int] = None,
        get_all_route: Union[bool, DEPENDENCIES] = True,
        get_one_route: Union[bool, DEPENDENCIES] = True,
        create_route: Union[bool, DEPENDENCIES] = True,
        update_route: Union[bool, DEPENDENCIES] = True,
        delete_one_route: Union[bool, DEPENDENCIES] = True,
        delete_all_route: Union[bool, DEPENDENCIES] = True,
        **kwargs: Any,
    ) -> None:
        # assert (
        #     tortoise_installed
        # ), "Tortoise ORM must be installed to use the TortoiseCRUDRouter."

        self.db_model = db_model
        self._pk: str = db_model.describe()["pk_field"]["db_column"]
        self._pk_type: type = get_pk_type(schema, self._pk)

        super().__init__(
            schema=schema,
            create_schema=create_schema,
            update_schema=update_schema,
            filter_schema=filter_schema,
            user_data_option=user_data_option,
            prefix=prefix or db_model.describe()["name"].replace("None.", ""),
            tags=tags,
            paginate=paginate,
            get_all_route=get_all_route,
            get_one_route=get_one_route,
            create_route=create_route,
            update_route=update_route,
            delete_one_route=delete_one_route,
            delete_all_route=delete_all_route,
            **kwargs,
        )

    def _get_all(self, *args: Any, **kwargs: Any) -> CALLABLE_LIST:
        async def route(pagination: PAGINATION = self.pagination) -> List[Model]:
            skip, limit = pagination.get("skip"), pagination.get("limit")

            query = self.db_model.all()
            total = await query.count()

            query = query.offset(cast(int, skip))
            if limit:
                query = query.limit(limit)
            objs = await query

            return resp_success(convert_to_pydantic(objs, self.schema), total=total)

        return route

    def _get_one(self, *args: Any, **kwargs: Any) -> CALLABLE:
        async def route(item_id: int) -> Model:
            obj = await self.db_model.get(**{self._pk: item_id})
            if obj:
                return resp_success(convert_to_pydantic(obj, self.schema))
            else:
                raise NOT_FOUND

        return route

    def _create(self, *args: Any, **kwargs: Any) -> CALLABLE:
        async def route(model: self.create_schema, request: Request) -> Model:  # type: ignore
            obj = await self.__create_obj_with_model(model, request, exclude={self._pk})
            return resp_success(convert_to_pydantic(obj, self.schema))

        return route

    def _update(self, *args: Any, **kwargs: Any) -> CALLABLE:
        async def route(
            item_id: int, model: self.update_schema  # type: ignore
        ) -> Model:
            await self.db_model.filter(id=item_id).update(
                **model.dict(exclude_unset=True)
            )
            return await self._get_one()(item_id)

        return route

    def _delete_all(self, *args: Any, **kwargs: Any) -> CALLABLE_LIST:
        async def route() -> List[Model]:
            await self.db_model.all().delete()
            return await self._get_all()(pagination={"skip": 0, "limit": None})

        return route

    def _delete_one(self, *args: Any, **kwargs: Any) -> CALLABLE:
        async def route(item_id: int) -> Model:
            ret = await self.db_model.filter(id=item_id).delete()
            return resp_success(bool(ret))

        return route

    #################################################################################
    def _kcreate(self, *args: Any, **kwargs: Any) -> CALLABLE:
        async def route(
            model: self.create_schema,  # type: ignore
            request: Request,
        ) -> RespModelT[Optional[self.schema]]:
            obj = await self.__create_obj_with_model(model, request, exclude={self._pk})
            return resp_success(convert_to_pydantic(obj, self.schema))

        return route

    def _kdelete_one(self, *args: Any, **kwargs: Any) -> CALLABLE:
        async def route(
            item_id: self._pk_type,
            _hard: bool = True,
        ) -> RespModelT[Optional[bool]]:
            if _hard is False:
                ret = await self.db_model.filter(
                    **{self._pk: item_id, "enabled_flag": 1}
                ).update(enabled_flag=0)
            else:
                ret = await self.db_model.filter(**{self._pk: item_id}).delete()

            return resp_success(bool(ret))

        return route

    def _kdelete_all(self, *args: Any, **kwargs: Any) -> CALLABLE_LIST:
        async def route(
            _hard: bool = True,
        ) -> RespModelT[Optional[int]]:
            if _hard is False:
                ret = await self.db_model.filter(enabled_flag=1).update(enabled_flag=0)
            else:
                ret = await self.db_model.all().delete()

            return resp_success(bool(ret))

        return route

    def _kupdate(self, *args: Any, **kwargs: Any) -> CALLABLE:
        async def route(
            model: self.schema,
            request: Request,
        ) -> RespModelT[Optional[self.schema]]:
            obj = await self.db_model.get(**{self._pk: getattr(model, self._pk)})

            if obj:
                await self.__update_obj_with_model(obj, model, request)
                return resp_success(convert_to_pydantic(obj, self.schema))
            else:
                raise ValueError("id不存在!")

        return route

    # 筛选
    def _kget_one_by_filter(self, *args: Any, **kwargs: Any) -> CALLABLE:
        async def route(
            filter: self.filter_schema,  # type: ignore
            request: Request,
            relationships: bool = False,
            user_data_filter: self.user_data_filter_type = self.user_data_filter_defv,
        ) -> RespModelT[Optional[self.schema]]:
            filter_dict = filter.model_dump(exclude_none=True)

            query = self.db_model.filter(enabled_flag=True)

            if (
                user_data_filter == UserDataFilter.SELF_DATA
                or user_data_filter == UserDataFilterSelf.SELF_DATA
            ):
                if hasattr(request.state, "user_id"):
                    query = query.filter(created_by=request.state.user_id)

            if filter_dict:
                query = query.filter(**filter_dict)

            if relationships:
                query = self.__autoload_options(query)

            obj = await query.first()

            # if relationships:
            #     await obj.fetch_related(self.db_model._meta.fetch_fields)

            if obj:
                return resp_success(
                    convert_to_pydantic(obj, self.schema, relationships)
                )
            else:
                raise NOT_FOUND

        return route

    # 自动加载选项函数
    def __autoload_options(self, query: QuerySet) -> QuerySet:
        return query.prefetch_related(*self.db_model._meta.fetch_fields)

    # list
    def _klist(self, *args: Any, **kwargs: Any) -> CALLABLE:
        async def route(
            request: Request,
            pagination: PAGINATION = self.pagination,
            sort_by: str = Query(None, description="Sort records by this field"),
            relationships: bool = False,
            user_data_filter: self.user_data_filter_type = self.user_data_filter_defv,
        ) -> RespModelT[Optional[List[self.schema]]]:
            skip, limit = pagination.get("skip"), pagination.get("limit")

            query = self.db_model.filter(enabled_flag=True)

            if (
                user_data_filter == UserDataFilter.SELF_DATA
                or user_data_filter == UserDataFilterSelf.SELF_DATA
            ):
                if hasattr(request.state, "user_id"):
                    query = query.filter(created_by=request.state.user_id)

            total = await query.count()

            if sort_by:
                query = query.order_by(sort_by)

            if skip:
                query = query.offset(cast(int, skip))

            if limit:
                query = query.limit(limit)

            if relationships:
                query = self.__autoload_options(query)

            objs = await query

            # if relationships:
            #     await objs.fetch_related(self.db_model._meta.fetch_fields)

            return resp_success(
                convert_to_pydantic(objs, self.schema, relationships), total=total
            )

        return route

    # 筛选
    def _kquery(self, *args: Any, **kwargs: Any) -> CALLABLE:
        async def route(
            filter: self.filter_schema,  # type: ignore
            request: Request,
            pagination: PAGINATION = self.pagination,
            sort_by: str = Query(None, description="Sort records by this field"),
            relationships: bool = False,
            user_data_filter: self.user_data_filter_type = self.user_data_filter_defv,
        ) -> RespModelT[Optional[List[self.schema]]]:
            filter_dict = filter.model_dump(exclude_none=True)

            skip, limit = pagination.get("skip"), pagination.get("limit")

            query = self.db_model.filter(enabled_flag=True)

            if (
                user_data_filter == UserDataFilter.SELF_DATA
                or user_data_filter == UserDataFilterSelf.SELF_DATA
            ):
                if hasattr(request.state, "user_id"):
                    query = query.filter(created_by=request.state.user_id)

            if filter_dict:
                query = query.filter(**filter_dict)

            total = await query.count()

            if sort_by:
                query = query.order_by(sort_by)

            if skip:
                query = query.offset(cast(int, skip))

            if limit:
                query = query.limit(limit)

            if relationships:
                query = self.__autoload_options(query)

            objs = await query

            # if relationships:
            #     await objs.fetch_related(self.db_model._meta.fetch_fields)

            return resp_success(
                convert_to_pydantic(objs, self.schema, relationships), total=total
            )

        return route

    # 筛选
    # Example query: [["age", ">=", 25], ["name", "=", "Alice"]]
    def _kquery_ex(self, *args: Any, **kwargs: Any) -> CALLABLE:
        async def route(
            query: List[Tuple[str, str, Union[str, int, float, datetime, List[Any]]]],
            request: Request,
            pagination: PAGINATION = self.pagination,
            sort_by: str = Query(None, description="Sort records by this field"),
            relationships: bool = False,
            user_data_filter: self.user_data_filter_type = self.user_data_filter_defv,
        ) -> RespModelT[Optional[List[self.schema]]]:
            skip, limit = pagination.get("skip"), pagination.get("limit")

            try:
                sql_query = self.db_model.filter(enabled_flag=True)

                if (
                    user_data_filter == UserDataFilter.SELF_DATA
                    or user_data_filter == UserDataFilterSelf.SELF_DATA
                ):
                    if hasattr(request.state, "user_id"):
                        sql_query = sql_query.filter(created_by=request.state.user_id)

                if query:
                    sql_query = parse_query(query, sql_query)

                if sort_by:
                    sql_query = sql_query.order_by(sort_by)

                total = await sql_query.count()

                if skip:
                    sql_query = sql_query.offset(cast(int, skip))

                if limit:
                    sql_query = sql_query.limit(limit)

                if relationships:
                    sql_query = self.__autoload_options(sql_query)

                objs = await sql_query

                # if relationships:
                #     await objs.fetch_related(self.db_model._meta.fetch_fields)

                return resp_success(
                    convert_to_pydantic(objs, self.schema, relationships), total=total
                )

            except Exception:
                raise HTTPException(
                    status_code=400, detail="Invalid query format or sort_by field"
                )

        return route

    # 插入冲突则更新
    def _kupsert(self, *args: Any, **kwargs: Any) -> CALLABLE:
        async def route(
            model: self.schema,  # type: ignore
            request: Request,
        ) -> RespModelT[Optional[self.schema]]:
            if hasattr(model, self._pk):
                item_id = getattr(model, self._pk)
                # obj = await self.db_model.get(**{self._pk: item_id})
                obj = await self.db_model.filter(**{self._pk: item_id}).first()
                if obj:
                    await self.__update_obj_with_model(obj, model, request)
                    return resp_success(
                        convert_to_pydantic(obj, self.schema), msg="update"
                    )

            obj = await self.__create_obj_with_model(model, request, exclude=None)
            return resp_success(convert_to_pydantic(obj, self.schema), msg="created")

            # model_dict = model.model_dump(exclude={self._pk}, exclude_none=True)
            # params = await self.handle_data(model_dict, True, request)
            # obj, created = await self.db_model.update_or_create( **{self._pk: item_id}, defaults=params )

        return route

    async def __create_obj_with_model(
        self, model, request: Request, exclude: IncEx = None
    ):
        model_dict = model.model_dump(exclude=exclude, exclude_none=True)
        params = await self.__handle_data(model_dict, True, request)
        obj = self.db_model(**params)
        await obj.save()
        return obj

    async def __update_obj_with_model(self, obj, model, request: Request):
        # 去掉关联对象
        model_dict = model.model_dump(
            exclude={self._pk, *self.db_model._meta.fetch_fields}, exclude_none=True
        )

        ##########################################################################################
        # Relationships
        relation_field = {
            key[:-7]: value
            for key, value in model_dict.items()
            if (value and key.endswith("_refids") and hasattr(self.db_model, key[:-7]))
        }

        obj_id = getattr(obj, self._pk)
        for rkey, rlist in relation_field.items():
            related_field = self.db_model._meta.fields_map[rkey]
            rclass = related_field.related_model
            rpk: str = rclass._meta.pk_attr

            filter_conditions = Q(**{f"{rpk}__in": rlist})
            if isinstance(related_field, fields.relational.BackwardFKRelation):
                rfield = related_field.relation_field
                update_val = {rfield: obj_id}
                none_val = {rfield: None}

                # 使用事务进行批量更新
                async with transactions.in_transaction():
                    # 1. 删掉所有指向obj_id的外键引用
                    await rclass.filter(**update_val).update(**none_val)
                    # 2. 更新关联数据的外键
                    await rclass.filter(filter_conditions).update(**update_val)
            elif isinstance(related_field, fields.relational.ManyToManyFieldInstance):
                rfield = related_field.model_field_name
                await obj.fetch_related(rfield)
                obj_related = getattr(obj, rfield)
                await obj_related.clear()
                filter_conditions = Q(**{f"{self._pk}__in": rlist})
                robjs = await rclass.filter(filter_conditions)
                for robj in robjs:
                    await obj_related.add(robj)
            else:
                pass

        ##########################################################################################

        params = await self.__handle_data(model_dict, False, request)

        # Update the fields with provided data
        for key, value in params.items():
            if hasattr(obj, key):
                setattr(obj, key, value)

        # Save the updated model instance
        await obj.save()

    async def __handle_data(
        self, data: Union[dict, list], create: bool, request: Request
    ) -> Union[dict, list]:
        """
        :param params: 参数列表
        :return: 过滤好的参数
        """
        if isinstance(data, dict):
            # 1. 只保留数据库字段
            # 2. 筛选掉的特定键列表

            db_model_fields = self.db_model._meta.fields_map.keys()

            keys_to_remove = ["creation_date", "updation_date", "enabled_flag"]
            params = {
                key: value
                for key, value in data.items()
                if ((key in db_model_fields) and (key not in keys_to_remove))
            }

            # 添加属性
            params["trace_id"] = getattr(request.state, "trace_id", 0)

            # User Info
            user_id = getattr(request.state, "user_id", 0)

            # if not params.get(self._pk, None):
            #     params["created_by"] = user_id

            if create:
                params["created_by"] = user_id

            params["updated_by"] = user_id

            return params

        if isinstance(data, list):
            params = [await self.__handle_data(item, create, request) for item in data]
            return params

        return data
