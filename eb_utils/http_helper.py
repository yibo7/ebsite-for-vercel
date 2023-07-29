from flask import request


def get_prams(key: str):
    s_value = None
    if request.method == 'POST':
        s_value = request.form.get(key, None)
    else:
        s_value = request.args.get(key, None)

    if s_value == 'None':  # 隐藏的Id控件默认是字符串的None
        s_value = None

    return s_value


def get_prams_dict():
    if request.method == 'POST':
        return request.form.to_dict()
    else:
        return request.args.to_dict()


def get_prams_int(key: str, default: int = 0) -> int:
    s_value = get_prams(key)
    if s_value:
        return int(s_value)
    return default


def get_prams_float(key: str, default: float = 0.0) -> float:
    s_value = get_prams(key)
    if s_value:
        return float(s_value)
    return default


def get_prams_bool(key: str, default: bool = False) -> bool:
    s_value = get_prams(key)
    if s_value:
        return bool(s_value)
    return default
