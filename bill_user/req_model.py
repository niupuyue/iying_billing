from pydantic import Field
from pydantic.networks import EmailStr

from bill_user.api_model import ArgsEmail


class ParamsUserLogin(ArgsEmail):
    """
    用户登录接口，请求参数对象
    """
    email = EmailStr
    password: str = Field(min_length=6, max_length=20)
