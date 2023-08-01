import uuid

from flask import request


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


def get_session_id():
    return request.cookies.get('session_id')
