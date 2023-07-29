import re


def FindStrToList(pattern, txt: str):
    """
    查找匹配的内容返回一个集合
    :param pattern: 正则表达式
    :param txt: 内容
    :return: 查找到的内容->list[str] 或 None
    """
    pt = re.compile(pattern, re.M | re.I)  # re.I 忽略大小写 re.M 多行模式
    rzs = pt.findall(txt)
    if rzs:
        return rzs
    return None


def FindOne(pattern, txt: str, index=0):
    """
    查找匹配的内容，但只返回指定组的值，默认第一个组
    :param pattern:正则表达式
    :param txt: 要查找的内容
    :param index: 指定组的索引
    :return: 返回查看到的字符
    """
    pt = re.compile(pattern, re.M | re.I | re.S)  # re.I 忽略大小写 re.M 多行模式 re.S 换行
    matchObj = pt.search(txt)
    if matchObj:
        return matchObj.group(index)
    return ""


def ReplaceAll(pattern: str, txt: str, replaceStr: str):
    """
    替换匹配到的字符
    :param pattern: 正则表达式
    :param txt: 要替换的内容
    :param replaceStr: 替换的字符，所有符合匹配条件的字条将被替换成此字符
    :return: 返回替换后的结果
    """
    return re.sub(pattern, replaceStr, txt)


def ReplaceCustom(pattern: str, txt: str, rpmethod):
    """
    将匹配的结果加工处理后再替换
    :param pattern: 正则表达式
    :param txt: 要替换的内容
    :param rpmethod: 指定一个方法返回替换后的值 如： rpmethod(matched) 参数matched是一个匹配结果 matched.group('value')
    :return: 返回替换后的结果
    """
    return re.sub(pattern, rpmethod, txt)


def IsMatch(pattern: str, txt: str) -> bool:
    matchObj = re.match(pattern, txt, re.M | re.I)  # match是严格要求从开始匹配的，非常适合做验证之类的匹配
    if matchObj:
        return True
    else:
        return False