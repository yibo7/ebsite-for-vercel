from flask import render_template, request, redirect

from bll.user_group import UserGroup
from entity.user_group_model import UserGroupModel
from website.pages_admin import admin_blue
from eb_utils import http_helper
from eb_utils.configs import WebPaths


# region class

@admin_blue.route('widget_list', methods=['GET'])
def widgets_list():
    ug = UserGroup()
    datas = ug.find_all()
    return render_template(WebPaths.get_admin_path("widgets/widget_list.html"), datas=datas)


@admin_blue.route('widget_list_save', methods=['GET', 'POST'])
def widgets_list_save():
    g_id = http_helper.get_prams('_id')
    model = UserGroupModel()
    bll = UserGroup()
    if g_id:
        model = bll.find_one_by_id(g_id)
    err = ''
    if request.method == 'POST':
        name = http_helper.get_prams('name')
        model.name = name
        if not bll.exist_name(name):
            bll.save(model)
            return redirect('widget_list')
        else:
            err = '已经存在相同名称的用户组'

    return render_template(WebPaths.get_admin_path("widgets/widget_list_save.html"), model=model, err=err)


@admin_blue.route('widget_list_del', methods=['GET', 'POST'])
def widgets_list_del():
    UserGroup().delete_from_page(http_helper.get_prams("ids"))
    return redirect("widget_list")


# endregion


