from typing import Any

from eb_utils import regex_utils


def is_string(obj: Any) -> bool:
    """
    判断对象是否为字符串
    :param obj:
    :return:
    """
    return isinstance(obj, str)


def is_number(input_string: str) -> bool:
    """
    判断字符是否为数字
    :param input_string:
    :return:
    """
    try:
        float(input_string)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(input_string)
        return True
    except (TypeError, ValueError):
        pass

    return False


def is_int(input_string: str) -> bool:
    """
    判断字符是否为整数
    >>> is_int('42') # returns true
    >>> is_int('42.0') # returns false

    :param input_string: String to check
    :type input_string: str
    :return: True if integer, false otherwise
    """
    return input_string.isdigit()


def is_decimal(input_string: str) -> bool:
    """
     判断字符是否为decimal
    >>> is_decimal('42.0') # returns true
    >>> is_decimal('42') # returns false

    :param input_string: String to check
    :type input_string: str
    :return: True if integer, false otherwise
    """
    return is_number(input_string) and '.' in input_string


def is_email(txt: str) -> bool:
    return regex_utils.IsMatch(r'[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)', txt)


def is_id_card(txt: str) -> bool:
    return regex_utils.IsMatch(
        r'[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]', txt)


def is_mobile(txt: str) -> bool:
    return regex_utils.IsMatch(r'1(3|4|5|6|7|8|9)\d{9}', txt)


def is_tel(txt: str) -> bool:
    return regex_utils.IsMatch(r'\d{3}-\d{8}|\d{4}-\d{7}', txt)


def is_ip(txt: str) -> bool:
    return regex_utils.IsMatch(r'((?:(?:25[0-5]|2[0-4]\d|[01]?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d?\d))', txt)


def is_post_code(txt: str) -> bool:
    return regex_utils.IsMatch(r'[1-9]\d{5}(?!\d)', txt)


def is_url(txt: str) -> bool:
    return regex_utils.IsMatch(r'[a-zA-z]+://[^\s]*', txt)
