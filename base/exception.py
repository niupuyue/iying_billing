from base import status, error_code


class IYingAPIExcepition(Exception):
    """
    异常基类
    """
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'


class PermissionDenied(IYingAPIExcepition):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'You do not have permission to perform this action.'


class UnauthorizedDenied(IYingAPIExcepition):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Unauthorized'


class BadRequestException(IYingAPIExcepition):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'bad request'

    def __init__(self, msg='', err_code=error_code.DEFAULT):
        self.error_code = err_code
        self.msg = msg

    def __str__(self):
        return self.msg or self.default_detail
