from secrets import token_hex
from typing import Type

from django.db.models import Model
from django_redis import get_redis_connection
from redis import Redis

from base import BadRequestException
from bill_user.models import BillUser


class UserSessionManager:

    def __init__(self, session_cache_key):
        """
        对应 settings.CACHES的key
        :param session_cache_key:
        """
        self.session_cache_key = session_cache_key
        self.__conn: Redis = get_redis_connection(self.session_cache_key)

    def get(self, token, model: Type[Model]):
        key = f'{model.__name__}:{token}'
        uid = self.__conn.get(key)
        return uid

    def set(self, uid, model: Type[Model]):
        token = token_hex(48)
        # token -> id
        # id - > token
        # before token
        before_token = self.__conn.get(uid)
        if before_token:
            self.__conn.delete(before_token)
        key = f'{model.__name__}:{token}'
        r1 = self.__conn.set(key, uid)
        r2 = self.__conn.set(uid, key)
        if r1 and r2:
            return token
        else:
            return None

    def delete(self, uid):
        # 清除用户信息缓存
        token = self.__conn.get(uid)
        if token is not None:
            self.__conn.delete(token)
            self.__conn.delete(uid)


userSessionManager = UserSessionManager('user_session')


def generate_login_session(user_id) -> str:
    # 生成 token
    token = userSessionManager.set(user_id, BillUser)
    if not token:
        raise BadRequestException('To generate the Token error')
    return token
