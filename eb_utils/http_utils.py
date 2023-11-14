import requests


def sort_parm(parm: {}):
    """
    将字典中的key排序，转换为地址参数字符串，往往API参数签名都需要使用到
    :param parm:
    :return:
    """
    str_parm = ''
    for p in sorted(parm):
        # 每次排完序的加到串中
        # str类型需要转化为url编码格式
        # if isinstance(parm[p], str):
        #     str_parm = f"{str_parm}{p}={parm[p]}&"  # str_parm + str(p) + "=" + str(quote(parm[p])) + "&"
        # continue
        # str_parm = str_parm + str(p) + "=" + str(parm[p]) + "&"
        str_parm = f"{str_parm}{p}={parm[p]}&"

    return str_parm


def request(url: str, method: str, param=None, headers=None, is_json=True, content_type: str = None, time_out=None,
            cookie=None, prox_url=None):
    """
    一个通用的http请求方法，目前只支持get与post,后期会更新
    :param prox_url:
    :param cookie: cookies 采用字典保存
    :param url: 请求的地址
    :param method: 请求的方法
    :param param:   请求参数，一个字典对象
    :param headers: 请求头，一个字典对象
    :param is_json: 返回的结果是否转换成json对象
    :param content_type: 请求时的Content-type类型，比如application/json
    :param time_out: 超时
    :return: 返回文本或json
    """
    try:
        prox = None
        if prox_url:
            prox = {
                'http': prox_url,
                'https': prox_url,
            }
        if method == 'get':
            r = requests.get(url=url, params=param, headers=headers, timeout=time_out, cookies=cookie, proxies=prox)
            r.encoding = r.apparent_encoding  # 服务器传过来的编码格式需要 先转换一下，再转成json格式 否则json格式的数据存在乱码
            result = r.json() if is_json else r.text  # 相当于问题表达式，意思是如果is_json不真，result=r.json()否则result = r.text
            return result
        elif method == 'post':
            if content_type == 'application/json':
                headers['Content-type'] = "application/json;charset=UTF-8"
                r = requests.post(url=url, json=param, headers=headers, timeout=time_out, cookies=cookie, proxies=prox)
                r.encoding = r.apparent_encoding
                result = r.json() if is_json else r.text
                return result
            else:
                r = requests.post(url=url, data=param, headers=headers, timeout=time_out, cookies=cookie, proxies=prox)
                r.encoding = r.apparent_encoding
                result = r.json() if is_json else r.text
                return result
        else:
            print("http method not allowed")
    except Exception as e:
        print("http请求报错:{0}".format(e))


def getText(url: str, params_obj={}, headers={}) -> str:
    """
    使用get方式请求地址
    :param url: 请求地址
    :param params_obj: 请求头，一个字典对象
    :param headers: 请求参数，一个字典对象
    :return: 返回文本
    """
    return request(url, "get", params_obj, headers, False)


def getJson(url: str, params_obj={}, headers={}) -> str:
    """
    使用get方式请求地址
    :param url: 请求地址
    :param params_obj: 请求参数，一个字典对象
    :param headers:  请求头，一个字典对象
    :return: 返回字典类型JSON对象
    """
    return request(url, "get", params_obj, headers, True)


def postText(url: str, params_obj={}, headers={}):
    """
    使用post方式请求地址
    :param url: 请求地址
    :param params_obj: 请求参数，一个字典对象
    :param headers: 请求头，一个字典对象
    :return: 返回文本
    """
    return request(url, "post", params_obj, headers, False)


def postJson(url: str, params_obj={}, headers={}):
    """
    使用post方式请求地址
    :param url: 请求地址
    :param params_obj: 请求参数，一个字典对象
    :param headers: 请求头，一个字典对象
    :return: 返回字典类型JSON对象
    """
    return request(url, "post", params_obj, headers, True)


def postJsonContent(url: str, content_obj={}, headers={}):
    """
    使用post方式请求地址,请求提交的内容为json
    :param url: 请求地址
    :param content_obj: 请求参数，一个字典对象
    :param headers: 请求头，一个字典对象
    :return: 返回字典类型JSON对象
    """
    return request(url, "post", content_obj, headers, True, "application/json")


def postFormContent(url: str, content_obj={}, headers={}, prox_url=None):
    """
    使用post方式请求地址,请求提交的内容为json
    :param prox_url:
    :param url: 请求地址
    :param content_obj: 请求参数，一个字典对象
    :param headers: 请求头，一个字典对象
    :return: 返回字典类型JSON对象
    """
    return request(url, "post", content_obj, headers, True, "application/x-www-form-urlencoded", prox_url=prox_url)
