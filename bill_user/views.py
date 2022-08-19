from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from django.views import View

from base import IYingBillAPIView, BadRequestException, error_code
from base.password import iying_check_password
from base.session import generate_login_session
from bill_user.models import BillUser, USER_STATUS
from bill_user.req_model import ParamsUserLogin
from bill_user.resp_model import RespUserLogin


class BillUserLoginView(IYingBillAPIView):
    """
    登录操作
    """
    # 调用该接口需要的权限
    permission_classes = ()
    # response 序列化对象
    method_response_model_map = dict(
        post=RespUserLogin,
    )

    def post(self, request, valid_args: ParamsUserLogin):
        # 判断该用户是否存在
        user: BillUser = BillUser.objects.filter((Q(email=valid_args.email) & Q(status=USER_STATUS[0])) | (
                Q(nickname=valid_args.email) & Q(status=USER_STATUS[0])))
        if not user:
            # 找不到该用户
            raise BadRequestException('该账号还未注册哦~')
        if not iying_check_password(valid_args.password, user.password):
            raise BadRequestException('登陆失败，用户名和密码错误，请重新登录一下~',
                                      error_code.PASSWORD_ERROR)
        # 生成新的token
        token = generate_login_session(user.id)
        return RespUserLogin(token=token,)
