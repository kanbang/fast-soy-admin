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


__all__ = ["UnitModel"]


