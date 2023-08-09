import inspect
import random
from dataclasses import replace

from flask import render_template_string, current_app
from markupsafe import Markup

from eb_utils import string_check
from entity.news_class_model import NewsClassModel


def __convert_to_number(value):
    if string_check.is_int(value):
        return int(value)
    elif string_check.is_decimal(value):
        return float(value)
    elif value == 'on':
        return True
    elif value == 'checkbox_unchecked':
        return False
    else:
        return value


def update_dic_to_class(dic_obj: {}, class_model):
    settings_dict = class_model.__dict__
    convert_dic = {key: __convert_to_number(value) for key, value in dic_obj.items()}
    settings_dict.update(convert_dic)
    settings_model_new = replace(class_model, **settings_dict)
    return settings_model_new


def random_int(min_value, max_value):
    return random.randint(min_value, max_value)


def random_float(min_value, max_value):
    return random.uniform(min_value, max_value)


def get_all_fields(model):
    attributes = []
    dic_f = model.__dict__
    if '_id' in dic_f:
        dic_f.pop('_id')
    # 获取当前类的属性
    for name, value in dic_f.items():
        attributes.append(name)

    fields_str = ", ".join(attributes)
    return fields_str
