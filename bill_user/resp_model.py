from pydantic.main import BaseModel

from bill_user.api_model import UserInfoModel


class RespUserLogin(BaseModel):
    """
    用户登录接口，返回内容对象
    """
    token: str
    user_info: UserInfoModel
