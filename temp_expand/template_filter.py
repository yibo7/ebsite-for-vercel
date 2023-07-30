"""
Custom filters, such as the "to_str" function, can be called in templates using the following method：
{% if item.get("_id")|to_str == model.reg_group_id %}
"""
from entity.user_group import UserGroup


def reg_temp_expand_filter(app):
    @app.template_filter()
    def to_str(value):
        return str(value)

    @app.template_filter()
    def to_user_group_name(gid):
        model = UserGroup().find_one_by_id(gid)
        if model:
            return model.get('name')
        return '不存在'

    @app.template_filter()
    def to_bool_name(truefalse:str):
        if truefalse and truefalse.lower() == 'true':
            return '是'
        else:
            return '否'