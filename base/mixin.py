import datetime
import time

from django.db import models
from django.db.models import Manager, QuerySet


class ModelMixin(models.Model):
    """
    数据库模型基类
    """
    objects: QuerySet = Manager()
    # model主键id
    id = models.AutoField(primary_key=True)
    # 创建时间
    create_time = models.BigIntegerField(default=time.time)
    # 更新时间
    update_time = models.BigIntegerField(default=time.time)
    # 是否删除
    deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.create_time = int(time.time())
        self.update_time = int(time.time())
        return super(ModelMixin, self).save(*args, **kwargs)

    def to_dict(self, fields=None) -> dict:
        """
        根据指定字段, 把orm对象转换成dict
        :param fields: list
        :return: dict
        """

        if fields is None:
            fields = self._meta.fields
        d = {}

        for column in fields:
            if isinstance(column, str):
                column_name = column
                value = getattr(self, column_name)
            else:
                column_name = column.name
                value = getattr(self, column_name)
            if isinstance(value, datetime.datetime):
                d[column_name] = value.strftime("%Y-%m-%d %H:%M:%S")
            elif value is None:
                d[column_name] = ""
            else:
                d[column_name] = value
        return d

    @classmethod
    def get_fields(cls) -> list:
        """
        获取模型定义的字段列表
        :return: list
        """
        return cls._meta.fields

    def __repr__(self):
        return f'<{self.__class__.__name__}:{self.id}>'

    __str__ = __repr__

    class Meta:
        abstract = True