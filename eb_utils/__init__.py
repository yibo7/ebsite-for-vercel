from dataclasses import replace

from eb_utils import string_check


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


def update_dic_to_dic(dic_from: dict, dic_to: dict):
    convert_dic = {key: __convert_to_number(value) for key, value in dic_from.items()}
    dic_to.update(convert_dic)
    return dic_to
