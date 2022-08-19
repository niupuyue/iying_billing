from django.db import models

# Create your models here.
from base.mixin import ModelMixin
from utils.time_format import generate_timestamp

USER_REGIST_SOURCE = [
    (1, 'android'),
    (2, 'ios'),
    (3, 'wechat'),
    (4, 'web'),
    (5, 'other')
]

USER_STATUS = [
    (1, 'active'),
    (2, 'dead'),
    (3, 'locked')
]

USER_GENDER = [
    (1, "女"),
    (2, "男"),
]

class BillUser(ModelMixin):
    nickname = models.CharField(verbose_name='用户昵称', default='', null=True, blank=True, max_length=30)
    email = models.EmailField(verbose_name='用户邮箱', null=True, blank=True)
    regist_source = models.SmallIntegerField(verbose_name='用户注册平台来源', choices=USER_REGIST_SOURCE, default=5, null=True,
                                             blank=True)
    mobile_phone = models.CharField(verbose_name='用户手机', default='', null=True, blank=True, max_length=15)
    password = models.CharField(verbose_name='用户密码', default='', null=False, blank=False, max_length=50)
    avatar = models.TextField(verbose_name='用户头像', default='', null=True, blank=True)
    gender = models.SmallIntegerField(verbose_name="用户性别", choices=USER_GENDER, default=USER_GENDER[0])

    class Meta:
        db_table = 'bill_user'
        ordering = ['-create_time']
