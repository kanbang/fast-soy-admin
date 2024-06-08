from pydantic import BaseModel, ConfigDict, Json
from datetime import datetime, date
from typing import List, Optional




class Ref_MfsDTO(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    desc: Optional[str] = None
    type_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)

class Ref_MfstDTO(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    desc: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class MfstCreateDTO(BaseModel):
    name: str
    desc: str
   
class MfstDTO(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    desc: Optional[str] = None
    mfss: Optional[List[Ref_MfsDTO]] = None
    mfss_refids: Optional[List[int]] = None

    model_config = ConfigDict(from_attributes=True)


class MfsCreateDTO(BaseModel):
    name: str
    desc: str
    type_id: Optional[int] = None


class MfsDTO(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    desc: Optional[str] = None
    type: Optional[Ref_MfstDTO] = None
    type_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)


class EquipmentCreateDTO(BaseModel):
    name: str
    type: Optional[int] = None
    parent_id: Optional[int] = None
    mfpts_refids: Optional[List[int]] = None
    mfsts_refids: Optional[List[int]] = None


class EquipmentDTO(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    type: Optional[int] = None
    parent_id: Optional[int] = None
    mfpts_refids: Optional[List[int]] = None
    mfsts_refids: Optional[List[int]] = None