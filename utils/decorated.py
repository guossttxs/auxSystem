from flask import request
from functools import wraps
from .util import load_params, set_result

def check_request_args(**params):
    '''
    检查请求的参数是否有误
    params: {
        'get': keys
        'post': keys
    }
    :return:
    '''
    def wrapper(func):
        @wraps(func)
        def _wrapper(*args, **kwargs):
            if 'get' in params:
                check_args = params.get('get')
                values = request.values
                if (set(values.keys()) & set(check_args)) != set(check_args):
                    return '缺少参数', 404
            if request.method == 'POST' and 'post' in params:
                check_args = params.get('post')
                data = load_params(request)
                if (set(data.keys()) & set(check_args)) != set(check_args):
                    return set_result(1, '缺少参数')
            return func(*args, **kwargs)
        return _wrapper
    return wrapper