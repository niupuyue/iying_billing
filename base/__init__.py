import inspect
import json
from json import JSONDecodeError
from typing import List, Type, Dict

from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import EmptyPage
from django.http import HttpResponse
from django.views import View
from pydantic import BaseModel, parse_obj_as
from pydantic.error_wrappers import ValidationError

from base.exception import PermissionDenied, UnauthorizedDenied, BadRequestException, IYingAPIExcepition
from base.permission import BasePermission, IsAuthenticated
from .log import iyingLogger
from utils import get_data
from .iying_response import make_iying_response


def user_role_check(user, role_list):
    if not role_list:
        return True

    if user.role not in role_list:
        return False
    else:
        return True


class IYingBillAPIView(View):
    permission_classes: List[Type[BasePermission]] = []
    pass_auth = []
    iyingLogger = iyingLogger
    method_response_model_map: Dict[str, BaseModel] = dict()
    permission_denied_class: Exception = PermissionDenied

    def check_permissions(self, request):
        for permission in self.get_permission():
            if not permission.has_permission(request, self):
                if isinstance(permission, IsAuthenticated):
                    raise UnauthorizedDenied()
                raise self.permission_denied_class()

        is_pass = user_role_check(request.user, self.pass_auth)
        if not is_pass:
            raise BadRequestException(
                '用户无权访问此接口'
                'The user does not have permission to access this interface'
            )

    def get_permission(self):
        return [permission() for permission in self.permission_classes]

    def handle_model_response(self, response, model):
        response_data = {}
        if model:
            if isinstance(response, dict):
                response_data = model.parse_obj(response)
                response_data = response_data.dict()
            elif isinstance(response, list):
                response_data = parse_obj_as(List[model], response)
                response_data = [r.dict() for r in response_data]
            elif response is None:
                response_data = {}
            else:
                # 单纯的mongo model 情况
                response_data = model.from_orm(response)
                response_data = response_data.dict()
        return response_data

    def dispatch(self, request: WSGIRequest, *args, **kwargs):
        """
        `.dispatch()` is pretty much the same as Django's regular dispatch,
        but with extra hooks for startup, finalize, and exception handling.
        """
        self.args = args
        self.kwargs = kwargs
        self.request = request
        _query_params = request.GET
        query_params = {}
        for key in _query_params:
            param = _query_params.getlist(key)
            if len(param) == 1:
                query_params[key] = param[0]
            else:
                item_list = []
                for item in param:
                    if "," not in item:
                        item_list.append(item)
                    else:
                        item_list.extend(item.split(','))
                query_params[key] = item_list
        try:
            # 检查权限
            self.check_permissions(request)
            request_method = request.method.lower()
            handler = getattr(self, request_method, None)
            if request_method not in self.http_method_names or handler is None:
                resp = self.http_method_not_allowed(request, *args, **kwargs)
                if resp:
                    resp_data = get_data(405, 'Method Not Allowed')
                    response = make_iying_response((resp_data))
                    self.response = response
                    return self.response
            signature = inspect.signature(handler)
            valid_args = signature.parameters.get('valid_args')
            if valid_args is not None:
                args_model = valid_args.annotation
            else:
                args_model = None
            args_data = None
            if args_model and args_model is not inspect.Parameter.empty:
                # request body loads
                if request_method in ['get']:
                    data = query_params
                else:
                    body = request.body
                    try:
                        data = json.loads(body)
                    except JSONDecodeError:
                        resp_data = get_data(400, 'Request body is not valid JSON')
                        response = make_iying_response(resp_data)
                        self.response = response
                        return self.response

                args_data = args_model.parse_obj(data)
            if args_model:
                args = [args_data, *args]
            response = handler(request, *args, **kwargs)
            if not isinstance(response, HttpResponse):
                response_data = response
                response_model = self.method_response_model_map.get(request_method)
                if response_model is not None:
                    response_data = self.handle_model_response(response, response_model)
                if response_data is None:
                    response_data = {}
                resp_data = get_data(200, 'success', response_data)
                response = make_iying_response(resp_data)
        except Exception as exc:
            if isinstance(exc, IYingAPIExcepition):
                msg = str(exc)
                err_code = None
                if not msg:
                    msg = exc.default_detail
                if isinstance(exc, BadRequestException):
                    err_code = exc.error_code
                resp_data = get_data(exc.status_code, msg, err_code=err_code)
            elif isinstance(exc, ValidationError):
                # 处理Pydantic参数校验异常
                msg = str(exc)
                err_code = 400
                resp_data = get_data(err_code, msg, err_code=err_code)
            elif isinstance(exc, EmptyPage):
                resp_data = get_data(200, "That page contains no results", data={})
            elif isinstance(exc, Ratelimited):
                resp_data = get_data(400, "Too many requests, please try again latter")
            else:
                if settings.DEBUG:
                    raise exc
                sunnyLogger.logger.exception(f'SunnyAPI exc ({exc})')
                resp_data = get_data(400, 'failed')
            response = make_sunny_response(resp_data)

        self.response = response

        return self.response
