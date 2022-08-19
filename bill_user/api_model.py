from pydantic import EmailStr, validator, ValidationError
from pydantic.main import BaseModel


class ArgsEmail(BaseModel):
    email: EmailStr

    @validator('email')
    def validate_email(cls, value: str):
        print('validate_email ({})'.format(value))
        l = value.split('@')
        username = l[0]
        domain = l[1]
        if not (1 <= len(username) <= 64 and 3 <= len(domain) < 255):
            raise ValidationError('Unsupported email address.')
        return value


class UserInfoModel(BaseModel):
    email: EmailStr
    nickname: str
    gender: str
    regist_source: str
    mobile_phone: str
    avatar: str
