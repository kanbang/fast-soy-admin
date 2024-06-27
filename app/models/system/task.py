
from tortoise import Model, fields


# Tortoise ORM models
class SchedulerTask(Model):
    id = fields.IntField(pk=True)
    job_class = fields.CharField(max_length=255)
    name = fields.CharField(max_length=255, null=True)
    group = fields.CharField(max_length=255, null=True)
    exec_strategy = fields.CharField(max_length=255)
    expression = fields.CharField(max_length=255)
    is_active = fields.BooleanField(default=True)
    create_datetime = fields.DatetimeField(auto_now_add=True)
    update_datetime = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "scheduler_task"

class SchedulerTaskRecord(Model):
    id = fields.IntField(pk=True)
    job_id = fields.CharField(max_length=255)
    job_class = fields.CharField(max_length=255, null=True)
    name = fields.CharField(max_length=255, null=True)
    group = fields.CharField(max_length=255, null=True)
    exec_strategy = fields.CharField(max_length=255, null=True)
    expression = fields.CharField(max_length=255, null=True)
    start_time = fields.DatetimeField()
    end_time = fields.DatetimeField()
    process_time = fields.FloatField()
    retval = fields.TextField(null=True)
    exception = fields.TextField(null=True)
    traceback = fields.TextField(null=True)
    create_datetime = fields.DatetimeField(auto_now_add=True)
    update_datetime = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "scheduler_task_record"