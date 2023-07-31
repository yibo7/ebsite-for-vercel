import re
import time

from flask import current_app

from eb_utils import string_check


def convert_to_type(value):
    if isinstance(value, str):
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
    return value


def annotation(value):
    def decorator(func):
        setattr(func, 'annotation', value)
        return func

    return decorator


class ModelBase:
    def __init__(self):
        self._id = None
        self.add_time = time.time()  # int(time.time())  # 只精确到秒

    def dict_to_model(self, dic_data: dict):
        for key, value in dic_data.items():
            setattr(self, key, convert_to_type(value))  #
        return self

    # def add_atr_setting(self, func, setting: str):
    #     func = self._add_annotation(setting)(func)

    def add_annotation(self, value):
        def decorator(func):
            setattr(func, 'annotation', value)
            return func
        return decorator

    def get_title(self, attribute_name: str):
        attribute = getattr(self, attribute_name)
        return getattr(attribute, 'annotation', None)

    def has_title(self, col):
        return hasattr(col, 'annotation')

    def get_titles(self):
        annotated_attributes = []

        for attribute_name in dir(self):
            attribute = getattr(self, attribute_name)
            if hasattr(attribute, 'annotation'):
                annotation_value = getattr(attribute, 'annotation')
                attribute_value = attribute.__get__(self)()

                filter_name = ''
                title = annotation_value
                if '|' in title:
                    a_title = title.split('|')
                    title = a_title[0]
                    filter_name = a_title[1]

                if filter_name:
                    attribute_value = current_app.jinja_env.filters[filter_name](str(attribute_value))

                annotated_attributes.append({
                    'title': title,
                    # 'col_name': attribute_name,
                    'value': attribute_value
                })

        return annotated_attributes
