import json
import pickle
import uuid
from typing import TypeVar

from flask import request

from db_utils import redis_db


def generate_key():
    return str(uuid.uuid4())


def get_safe_coe_key():
    sid = request.session_id
    if sid:
        return f'safe_code_{sid}'
    return None

def get_str(key: str) -> str:
    if key:
        v = redis_db.get(key)
        return v.decode('utf-8') if v else ""
    return ""


def get_obj(key: str):
    if key:
        # 从Redis中获取保存的二进制数据
        binary_data = redis_db.get(key)
        if binary_data:
            # 将二进制数据转换回字典对象
            data_obj = pickle.loads(binary_data)
            return data_obj
    return None


def exists_key(key: str):
    # 检查键是否存在
    return redis_db.exists(key)


def clear():
    # 清空数据库
    redis_db.flushdb()


def get_all_keys():
    return redis_db.keys('*')


def delete(key: str):
    redis_db.delete(key)


def set_obj(obj, ex_second=0, key=None):
    """
    设置一个缓存对象
    :param key: 键，如果不设置会自动生成一个
    :param obj: 要保存的对象
    :param ex_second: 过期时间，以秒为单位，如果不填写或0将永久保存
    :return: 返回 key值
    """

    if not key:
        key = generate_key()

    if not (isinstance(obj, str) or isinstance(obj, int) or isinstance(obj, float)):
        # 序列化字典为 JSON 字符串
        # obj = json.dumps(obj)
        # 将字典对象转换为二进制数据
        obj = pickle.dumps(obj)

    if ex_second:
        redis_db.set(key, obj, ex=ex_second)
    else:
        redis_db.set(key, obj)

    return key


def set_ex_minutes(obj, ex_minutes: int, key=None):
    """
    设置一个缓存对象-过期时间以分钟为单位
    :param key: 键
    :param obj: 要保存的对象
    :param ex_minutes: 过期时间，以分钟为单位
    :return:
    """
    expiration_seconds = ex_minutes * 60
    return set_obj(obj, expiration_seconds, key)


def set_ex_hours(obj, ex_hours: int, key=None):
    """
   设置一个缓存对象-过期时间以小时为单位
   :param key: 键
   :param obj: 要保存的对象
   :param ex_hours: 过期时间，以小时为单位
   :return:
   """
    expiration_seconds = ex_hours * 60 * 60
    return set_obj(obj, expiration_seconds, key)


def generate_next_id(key):
    """
    生成某个键下的自增Id
    :param key:
    :return:
    """
    return redis_db.incr(key)


def add_count_second(key, ex_second=60):
    """
    生成某个键下的自增值，并过期会自动清理
    :param key:
    :return:
    """
    new_value = redis_db.incr(key)
    # 设置过期时间为60秒
    redis_db.expire(key, ex_second)
    return new_value


def add_count_minute(key, ex_minutes=60):
    expiration_seconds = ex_minutes * 60
    return add_count_second(key, expiration_seconds)


def add_count_hour(key, ex_hours=60):
    expiration_seconds = ex_hours * 60 * 60
    return add_count_second(key, expiration_seconds)


def get_count(key):
    i_count = get_str(key)
    if i_count:
        return int(i_count)
    return 0
