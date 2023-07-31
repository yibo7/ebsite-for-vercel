from flask import render_template, request, redirect

from bll.user import User
from bll.user_group import UserGroup
from entity.user_group_model import UserGroupModel
from entity.user_model import UserModel
from website.pages_admin import admin_blue
from eb_utils import http_helper, get_table_html
from eb_utils.configs import WebPaths


# region user-group

@admin_blue.route('user_group', methods=['GET'])
def user_group():
    ug = UserGroup()
    datas = ug.find_all()
    return render_template(WebPaths.get_admin_path("user/user_group.html"), datas=datas)


@admin_blue.route('user_group/save', methods=['GET', 'POST'])
def user_group_add():
    g_id = http_helper.get_prams('id')
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
            return redirect('../user_group')
        else:
            err = '已经存在相同名称的用户组'

    return render_template(WebPaths.get_admin_path("user/user_group_save.html"), model=model, err=err)


@admin_blue.route('user_group/del', methods=['GET', 'POST'])
def user_group_del():
    UserGroup().delete_from_page(http_helper.get_prams("ids"))
    return redirect("../user_group")


# endregion

# region users


@admin_blue.route('user_list', methods=['GET'])
def user_list():
    keyword = http_helper.get_prams("k")
    page_num = http_helper.get_prams_int("p", 1)
    bll = User()
    datas, pager = bll.search(keyword, page_num, 'username')

    del_btn = {"show_name": "删除", "url": "user_list_del?ids=#_id#", "confirm": True}
    modify_btn = {"show_name": "修改", "url": "user_list_save?id=#_id#", "confirm": False}

    table_html = get_table_html(datas, [del_btn, modify_btn])

    return render_template(WebPaths.get_admin_path("user/user_list.html"), table_html=table_html, pager=pager,
                           datas=datas)


@admin_blue.route('user_list_save', methods=['GET', 'POST'])
def user_list_save():
    data_id = http_helper.get_prams('id')
    model = UserModel()
    bll = User()
    if data_id:
        model = User().find_one_by_id(data_id)

    err = ''
    if request.method == 'POST':
        dic_prams = http_helper.get_prams_dict()
        model.dict_to_model(dic_prams)
        _id = bll.save(model)
        return redirect('user_list')
    group = UserGroup().find_all()
    return render_template(WebPaths.get_admin_path("user/user_list_save.html"), model=model, group=group, err=err)


@admin_blue.route('user_list_del', methods=['GET', 'POST'])
def user_list_del():
    User().delete_from_page(http_helper.get_prams("ids"))
    return redirect("user_list")

# endregion
