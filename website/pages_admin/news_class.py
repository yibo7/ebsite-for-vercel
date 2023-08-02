from flask import render_template, request, redirect

from bll.user_group import UserGroup
from entity.user_group_model import UserGroupModel
from website.pages_admin import admin_blue
from eb_utils import http_helper
from eb_utils.configs import WebPaths


# region class

@admin_blue.route('class_list', methods=['GET'])
def class_list():
    ug = UserGroup()
    datas = ug.find_all()
    return render_template(WebPaths.get_admin_path("news_class/class_list.html"), datas=datas)


@admin_blue.route('class_list_save', methods=['GET', 'POST'])
def class_list_save():
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
            return redirect('class_list')
        else:
            err = '已经存在相同名称的用户组'

    return render_template(WebPaths.get_admin_path("news_class/class_list_save.html"), model=model, err=err)


@admin_blue.route('class_list_del', methods=['GET', 'POST'])
def class_list_del():
    UserGroup().delete_from_page(http_helper.get_prams("ids"))
    return redirect("class_list")


# endregion

# region template

@admin_blue.route('class_temp_list', methods=['GET'])
def class_temp_list():
    ug = UserGroup()
    datas = ug.find_all()
    return render_template(WebPaths.get_admin_path("news_class/class_temp_list.html"), datas=datas)


@admin_blue.route('class_temp_list_save', methods=['GET', 'POST'])
def class_temp_list_save():
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
            return redirect('class_temp_list')
        else:
            err = '已经存在相同名称的用户组'

    return render_template(WebPaths.get_admin_path("news_class/class_temp_list_save.html"), model=model, err=err)


@admin_blue.route('class_temp_list_del', methods=['GET', 'POST'])
def class_temp_list_del():
    UserGroup().delete_from_page(http_helper.get_prams("ids"))
    return redirect("class_temp_list")


# endregion

