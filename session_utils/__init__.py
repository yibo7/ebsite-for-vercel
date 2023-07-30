import uuid

from flask import request, make_response


# def check_session(func):
#     def wrapper(*args, **kwargs):
#         session_id = request.cookies.get('session_id')
#         if not session_id:
#             session_id = str(uuid.uuid4())  # 生成一个新的 Session ID
#             # 在这里可以将生成的 Session ID 存储到 Redis 或其他适合的存储介质中
#             # 例如：redis.set(session_id, {})
#             response = make_response()
#             response.set_cookie('session_id', session_id)  # 将 Session ID 设置到响应的 Cookie 中
#             request.session_id = session_id  # 将 Session ID 存储到请求对象中，以便后续使用
#         else:
#             request.session_id = session_id  # 将已存在的 Session ID 存储到请求对象中
#         return func(*args, **kwargs)
#
#     return wrapper

def check_session(func):
    def wrapper(*args, **kwargs):
        session_id = request.cookies.get('session_id')
        if not session_id:
            session_id = str(uuid.uuid4())  # 生成一个新的 Session ID
            # 在这里可以将生成的 Session ID 存储到 Redis 或其他适合的存储介质中
            # 例如：redis.set(session_id, {})
            response = make_response()
            response.set_cookie('session_id', session_id)  # 将 Session ID 设置到响应的 Cookie 中
            request.session_id = session_id  # 将 Session ID 存储到请求对象中，以便后续使用
            return response  # 返回响应对象
        else:
            request.session_id = session_id  # 将已存在的 Session ID 存储到请求对象中
        return func(*args, **kwargs)

    return wrapper


def get_session_id():
    return request.cookies.get('session_id')
