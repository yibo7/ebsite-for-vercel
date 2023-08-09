"""
Custom filters, such as the "to_str" function, can be called in templates using the following method：
{% if item.get("_id")|to_str == model.reg_group_id %}
"""
from datetime import datetime

from bll.user_group import UserGroup
from bll.widgets import Widgets


def reg_temp_expand_filter(app):
    @app.template_filter()
    def to_str(value):
        return str(value)

    @app.template_filter()
    def to_user_group_name(gid):
        model = UserGroup().find_one_by_id(gid)
        if model:
            return model.name
        return '不存在'

    @app.template_filter()
    def to_bool_name(truefalse: str):
        if truefalse and truefalse.lower() == 'true':
            return '是'
        else:
            return '否'

    @app.template_filter()
    def adminer_status(truefalse: int):
        if truefalse == 1:
            return '正常'
        else:
            return '不正常'

    @app.template_filter()
    def widget_type_name(data_id: int):
        t = Widgets().get_type_by_id(int(data_id))
        if t:
            return t.get('name')
        return 'can`t find type'

    @app.template_filter()
    def to_time_name(timestamp):
        dt = datetime.fromtimestamp(float(timestamp))
        formatted_time = dt.strftime("%Y-%m-%d %H:%M")
        return formatted_time
