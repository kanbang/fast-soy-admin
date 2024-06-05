from pydantic import BaseModel, ConfigDict, Json
from datetime import datetime, date
from typing import Optional


class UnitCreateDTO(BaseModel):
    unitid: str
    name: str
    code: str
    group: str
    plant: str
    power: str
    type: str
    axis_code: str
    axis_catalog: str
    tsi: str
    tdm: str
    manufacturer: str
    cooling: str
    gen_cooling: str
    heat_supply: bool
    last_overhaul: datetime
    info_update: datetime
    rod_start: datetime
    mfg_date: datetime
    install_desc: str
    crit_speed: float

    # class Config:
    #     orm_mode = True
    #     # 此选项将允许我们将ORM对象实例转换为Pydantic对象实例 from_orm

class UnitDTO(BaseModel):
    unitid: Optional[str] = None
    name: Optional[str] = None
    code: Optional[str] = None
    group: Optional[str] = None
    plant: Optional[str] = None
    power: Optional[str] = None
    type: Optional[str] = None
    axis_code: Optional[str] = None
    axis_catalog: Optional[str] = None
    tsi: Optional[str] = None
    tdm: Optional[str] = None
    manufacturer: Optional[str] = None
    cooling: Optional[str] = None
    gen_cooling: Optional[str] = None
    heat_supply: Optional[bool] = None
    last_overhaul: Optional[datetime] = None
    info_update: Optional[datetime] = None
    rod_start: Optional[datetime] = None
    mfg_date: Optional[datetime] = None
    install_desc: Optional[str] = None
    crit_speed: Optional[float] = None

    # V2
    model_config = ConfigDict(from_attributes=True)

    # V1
    # class Config:
    #     orm_mode = True
    #     from_attributes
