# @author:Niu Puyue
# e-mail:niupuyue@aliyun.com
# time:2022/6/16 9:41 PM
# desc:


def get_data(status_code, msg, data=None, err_code=None):
    """
    封装 data
    """
    result = {
        "code": status_code,
        "msg": msg,
        "data": data,
    }

    if err_code:
        result['error_code'] = err_code

    return result
