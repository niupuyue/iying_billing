class BasePermission(object):
    """
    权限基类
    """

    def has_permission(self, request, view):
        return True


class IsAuthenticated(BasePermission):
    # 是否已经通过身份认证
    def has_permission(self, request, view):
        return request.user
