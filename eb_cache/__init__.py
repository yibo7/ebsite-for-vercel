import os
import pickle
import uuid

from flask import current_app
from flask_caching import Cache

from eb_utils.xs_json import XsJson

SettingModel = {
    "MongoDBUrl": "",
    "RedisUrl": "",
    "API_KEY": ""
}

cache: Cache = None


def init_eb_cache(app):

    cf_path = 'conf/setting.json'

    # 检查文件是否存在
    CF_APP = {}
    if os.path.exists(cf_path):
        CF = XsJson("conf/setting.json")
        CF_APP = CF.load()

    else:
        print(f"在vercel上运行忽略setting.json请在环境变量设置配置。")

    REDIS_SERV = os.environ.get('REDIS_SERV', CF_APP.get('RedisUrl'))

    cache_config = {
        'CACHE_TYPE': 'SimpleCache'  # 默认设置为SimpleCache
    }
    if REDIS_SERV:  # 如果REDIS_SERV不为空
        cache_config['CACHE_TYPE'] = 'RedisCache'
        cache_config['CACHE_REDIS_URL'] = REDIS_SERV

    global cache
    cache = Cache(config=cache_config)
    cache.init_app(app)
    app.config.update({'base_settings': CF_APP})


def base_setting() -> SettingModel:
    return current_app.config['base_settings']

def base_setting_value(key: str) -> str:
    model = base_setting()
    if not model:
        raise ValueError(f"base_setting为空")
    if key in model:
        return model[key]
    raise ValueError(f"base_setting不存在{key}")


def generate_key():
    return str(uuid.uuid4())


def get_str(key: str) -> str:
    if key:
        v = cache.get(key)
        return v.decode('utf-8') if v else ""
    return ""


def get(key: str, default_value=None):
    value = cache.get(key)
    if value:
        return value
    return default_value


def get_obj(key: str):
    if key:
        # 从Redis中获取保存的二进制数据
        binary_data = cache.get(key)
        if binary_data:
            # 将二进制数据转换回字典对象
            data_obj = pickle.loads(binary_data)
            return data_obj
    return None

def set_data(obj, ex_second=0, key=None):
    """
    设置一个缓存对象
    :param key: 键，如果不设置会自动生成一个
    :param obj: 要保存的对象
    :param ex_second: 过期时间，以秒为单位，如果不填写或0将永久保存
    :return: 返回 key值
    """
    if not key:
        key = generate_key()

    if ex_second:
        cache.set(key, obj, timeout=ex_second)
    else:
        cache.set(key, obj, timeout=None)  # 永久缓存

    return key

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

    # 序列化对象为 JSON 字符串
    obj = obj if isinstance(obj, (str, int, float)) else pickle.dumps(obj)

    if ex_second:
        cache.set(key, obj, timeout=ex_second)
    else:
        cache.set(key, obj, timeout=None)  # 永久缓存

    return key


def set_ex_hours(obj, ex_hours: int, key=None):
    """
   设置一个缓存对象-过期时间以小时为单位
   :param key: 键
   :param obj: 要保存的对象
   :param ex_hours: 过期时间，以小时为单位
   :return: 返回缓存的键
   """
    expiration_seconds = ex_hours * 60 * 60
    return set_obj(obj, expiration_seconds, key)


def exists_key(key: str) -> bool:
    # 检查键是否存在
    cached_value = cache.get(key)
    if cached_value is not None:
        return True
    else:
        return False


def clear():
    # 清空数据库
    cache.clear()


# def get_all_keys():
#     return redis_db.keys('*')


def delete(key: str):
    """
    删除一个缓存
    """
    cache.delete(key)


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


# def generate_next_id(key):
#     """
#     生成某个键下的自增Id
#     :param key:
#     :return:
#     """
#     return redis_db.incr(key)

def next_id(key, timeout=None):
    """
    生成某个键下的自增Id，如果键不存在，则从 initial 开始
    :param key: 缓存键
    :param timeout: 缓存超时时间
    :return: 当前的值
    """

    # 尝试获取当前值，如果键不存在则返回初始值
    current_value = cache.get(key)
    if not current_value:
        current_value = 0  # 如果键不存在时的初始值
    print(current_value)
    # 将值加一，并设置回缓存，超时时间由参数决定
    new_value = current_value + 1
    cache.set(key, new_value, timeout=timeout)
    return new_value
