import json
import sys
from facePhoto.utils.FPExceptions import FormException
from facePhoto.utils.FPResponse import FPResponse


def request_decorator(func):
    def wrapper(*args, **kw):
        try:
            data = func(*args, **kw)
        except FormException as e:
            if e.raw_exception:
                sys.stderr.write(str(e.raw_exception))
            return FPResponse.failure(e.message)
        return FPResponse.success(data)

    return wrapper


def login_decorator(func):
    def wrapper(request, *args, **kw):
        user = request.session.get('user')
        if not user:
            raise FormException('请先登录')
        return func(request, *args, **kw)

    return wrapper


def dump_form_data(func):
    def wrapper(request, *args, **kw):
        try:
            form_data = json.loads(request.body)
        except json.JSONDecodeError:
            raise FormException('表单数据异常')
        return func(request, form_data, *args, **kw)

    return wrapper
