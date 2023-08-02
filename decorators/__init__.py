import uuid
from functools import wraps

from flask import request, g

from bll.site_log import SiteLog
from eb_utils import http_helper
from entity.site_log_model import SiteLogModel
from entity.user_token import UserToken


def check_session(func):
    def wrapper(response):
        session_id = request.cookies.get('session_id')
        if not session_id:
            session_id = str(uuid.uuid4())  # 生成一个新的 Session ID
            response.set_cookie('session_id', session_id)  # 将 Session ID 设置到响应的 Cookie 中
            # request.session_id = session_id  # 将 Session ID 存储到请求对象中，以便后续使用

        # else:
        #     request.session_id = session_id  # 将已存在的 Session ID 存储到请求对象中
        return func(response)

    return wrapper


def admin_action_log(title: str):
    # 在工厂函数内部定义装饰器
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            content = f"执行函数：{func.__name__}，参数：{args}{kwargs}"
            # SiteLog().add_log(title,content)
            model = SiteLogModel()
            model.title = title
            model.description = content
            model.url = http_helper.get_url_full()
            model.ip_addr = http_helper.get_ip()

            user = g.u
            if user:
                model.user_name = user.name
                model.ni_name = user.ni_name
                model.user_id = user.id
            SiteLog().add(model)
            return func(*args, **kwargs)
        return wrapper
    return decorator
