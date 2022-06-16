from django.db import models

# Create your models here.
from utils.time_format import generate_timestamp


class BaseUser(models.Model):
    USER_STATUS = [
        (1, 'active'),
        (2, 'dead'),
        (3, 'locked')
    ]
    status = models.SmallIntegerField(verbose_name='用户状态', choices=USER_STATUS, default=1, null=True, blank=True)
    create_time = models.BigIntegerField(verbose_name='创建时间', default=generate_timestamp(), null=True, blank=True)
    update_time = models.BigIntegerField(verbose_name='更新时间', default=generate_timestamp(), null=True, blank=True)

    class Meta:
        abstract = True


class BillUser(BaseUser):
    USER_REGIST_SOURCE = [
        (1, 'android'),
        (2, 'ios'),
        (3, 'wechat'),
        (4, 'web'),
        (5, 'other')
    ]
    nickname = models.CharField(verbose_name='用户昵称', default='', null=True, blank=True, max_length=30)
    email = models.EmailField(verbose_name='用户邮箱', null=True, blank=True)
    regist_source = models.SmallIntegerField(verbose_name='用户注册平台来源', choices=USER_REGIST_SOURCE, default=5, null=True,
                                             blank=True)
    mobile_phone = models.CharField(verbose_name='用户手机', default='', null=True, blank=True, max_length=15)
    password = models.CharField(verbose_name='用户密码', default='', null=False, blank=False, max_length=50)
    avatar = models.TextField(verbose_name='用户头像', default='', null=True, blank=True)

    class Meta:
        db_table = 'bill_user'
        ordering = ['-create_time']
