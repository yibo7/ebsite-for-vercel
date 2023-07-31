"""
Custom global functions can be called in templates using the following method：
{{say_hello('cqs')}}
"""
from markupsafe import Markup

from entity.select_opt import SelectItem


def reg_temp_expand_fun(app):
    @app.template_global()
    def say_hello(msg: str):
        return Markup(f'<h1>你好呀:{msg}</h1>')

    @app.template_global()
    def build_sel_item(datas, value_key: str, name_key: str, sel_value: str):
        select_html = []
        for data in datas:
            name = 'none'
            value = 'none'
            if hasattr(data, name_key):
                name = getattr(data, name_key) # data[name_key]
            if hasattr(data, value_key):
                value = getattr(data, value_key) # data[value_key]
            if str(value) == sel_value:
                select_html.append(f'<option selected value="{value}">{name}</option>')
            else:
                select_html.append(f'<option  value="{value}">{name}</option>')

        return Markup(''.join(select_html))
