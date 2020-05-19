import re

from facePhoto.models import User
from facePhoto.utils.FPDecorator import request_decorator, login_decorator, dump_form_data
from facePhoto.utils.FPExceptions import FormException


@request_decorator
@dump_form_data
def login(request, form_data):
    mobile = form_data.get('mobile')
    username = form_data.get('username')
    password = form_data.get('password')

    if not mobile and not username:
        raise FormException('用户名或手机号为空')
    if mobile and not re.match(r'^[1]([3-9])[0-9]{9}$', mobile):
        raise FormException('手机号不合法')
    if not password:
        raise FormException('密码为空')
    try:
        if mobile:
            db_user = User.objects.values().get(mobile=mobile)
        else:
            db_user = User.objects.values().get(username=username)
    except User.DoesNotExist:
        raise FormException('用户不存在')
    if db_user.get('password') != password:
        raise FormException('密码错误')
    del db_user['password']
    request.session['user'] = db_user
    return "登录成功"


@request_decorator
@dump_form_data
def register(request, form_data):
    username = form_data.get('username')
    if not username or len(username) < 3 or len(username) > 10:
        raise FormException('用户名不合法')
    if User.objects.filter(username=username).count() > 0:
        raise FormException('用户名已存在')
    password = form_data.get('password')
    if not password or len(password) < 6 or len(password) > 20:
        raise FormException('密码不合法')
    mobile = form_data.get('mobile')

    if not mobile or not re.match(r'^[1]([3-9])[0-9]{9}$', mobile):
        raise FormException('手机号不合法')
    if User.objects.filter(mobile=mobile).count() > 0:
        raise FormException('手机号已存在')
    user = User(username=username, mobile=mobile, password=password)
    try:
        user.save()
        return "注册成功"
    except Exception as e:
        raise e


@request_decorator
@login_decorator
def currentUser(request):
    user = request.session.get('user')
    return user


@request_decorator
@login_decorator
def logout(request):
    request.session.clear()
    return "退出成功"
