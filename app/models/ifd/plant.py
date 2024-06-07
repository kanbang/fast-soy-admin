from enum import Enum
from tortoise import fields
from app.models.base import KBaseModel

class UnitModel(KBaseModel):
    """记录表"""

    unitid = fields.CharField(max_length=255, null=False)
    name = fields.CharField(max_length=255, null=False)
    code = fields.CharField(max_length=255, null=False)
    group = fields.CharField(max_length=255, description="集团")
    plant = fields.CharField(max_length=255, description="电厂")
    power = fields.CharField(max_length=255, description="功率")
    type = fields.CharField(max_length=255, description="型号")
    axis_code = fields.CharField(max_length=255, description="轴系编码")
    axis_catalog = fields.CharField(max_length=255, description="轴系目录")
    tsi = fields.CharField(max_length=255, description="TSI配置")
    tdm = fields.CharField(max_length=255, description="TDM配置")
    manufacturer = fields.CharField(max_length=255, description="制造厂商")
    cooling = fields.CharField(max_length=255, description="冷凝方式")
    gen_cooling = fields.CharField(max_length=255, description="发电机冷却方式")
    heat_supply = fields.BooleanField(default=False, description="是否供热")
    last_overhaul = fields.DateField(description="最后一次大修时间")
    info_update = fields.DateField(description="信息更新时间")
    rod_start = fields.DateField(description="投产时间")
    mfg_date = fields.DateField(description="制造日期")
    install_desc = fields.TextField(description="安装过程描述")
    crit_speed = fields.FloatField(description="临界转速")

    class Meta:
        table = "unit"


class Equipment(KBaseModel):
    id = fields.IntField(pk=True, description="ID")
    name = fields.CharField(max_length=100, description="名称")
    type = fields.IntField(default=0, description="类型")
    parent_id = fields.IntField(default=0, max_length=10, description="父菜单ID")
    mfpts = fields.ManyToManyField("app_system.MFPT", related_name="equipments")
    mfsts = fields.ManyToManyField("app_system.MFST", related_name="equipments")

    class Meta:
        table = "equipment"

# 机器故障现象类型 MFP (Machine Fault Phenomena Type)
class MFPT(KBaseModel):
    id = fields.IntField(pk=True, description="ID")
    name = fields.CharField(max_length=100, description="名称")
    desc = fields.CharField(max_length=200, description="描述")

    class Meta:
        table = "mfpt"

# 机器故障现象 MFP (Machine Fault Phenomena)
class MFP(KBaseModel):
    id = fields.IntField(pk=True, description="ID")
    name = fields.CharField(max_length=100, description="名称")    
    type = fields.ForeignKeyField("app_system.MFPT", related_name="mfps")
    desc = fields.CharField(max_length=200, description="描述")

    class Meta:
        table = "mfp"

# 机器故障征兆类型 MFST (Machine Fault Symptoms Type) 
class MFST(KBaseModel):
    id = fields.IntField(pk=True, description="ID")
    name = fields.CharField(max_length=100, description="名称")
    desc = fields.CharField(max_length=200, description="描述")

    class Meta:
        table = "mfst"

# 机器故障征兆 MFS (Machine Fault Symptoms) 
class MFS(KBaseModel):
    id = fields.IntField(pk=True, description="ID")
    name = fields.CharField(max_length=100, description="名称")
    type = fields.ForeignKeyField("app_system.MFST", related_name="mfss")
    desc = fields.CharField(max_length=200, description="描述")

    class Meta:
        table = "mfs"


__all__ = ["UnitModel", "Equipment", "MFPT", "MFP", "MFST", "MFS"]


