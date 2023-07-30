from flask import render_template, request, redirect

from website.pages_admin import admin_blue
from eb_utils import http_helper, get_table_data, update_dic_to_dic
from eb_utils.configs import WebPaths
from entity.user import User
from entity.user_group import UserGroup


# region user-group

@admin_blue.route('user_group', methods=['GET'])
def user_group():
    ug = UserGroup()
    datas = ug.find_all()
    return render_template(WebPaths.get_admin_path("user/user_group.html"), datas=datas)


@admin_blue.route('user_group/save', methods=['GET', 'POST'])
def user_group_add():
    g_id = http_helper.get_prams('id')
    model = UserGroup().__dict__
    if g_id:
        model = UserGroup().find_one_by_id(g_id)
    err = ''
    if request.method == 'POST':
        name = http_helper.get_prams('name')
        model['name'] = name
        if not UserGroup().exist_name(name):
            UserGroup().save(model)
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
    datas, pager = User().search(keyword, page_num, 'username')

    # cols = {
    #     "id": "ID",
    #     "user_name": "账号",
    #     "real_name": "真实改名",
    #     "mobile": "手机号",
    #     "create_time": "添加时间",
    # }
    # del_btn = {"show_name": "删除", "url": "user_list_del?id=#ID#", "confirm": True}
    # modify_btn = {"show_name": "修改", "url": "user_list_save?id=#ID#", "confirm": False}
    #
    # [tb_header, tb_items] = get_table_data(datas, cols, [del_btn, modify_btn])

    return render_template(WebPaths.get_admin_path("user/user_list.html"), pager=pager, datas=datas)


@admin_blue.route('user_list_save', methods=['GET', 'POST'])
def user_list_save():
    g_id = http_helper.get_prams('id')
    model = User().__dict__
    if g_id:
        model = User().find_one_by_id(g_id)
    err = ''
    if request.method == 'POST':
        dic_prams = http_helper.get_prams_dict()
        update_dic_to_dic(dic_prams, model)
        _id = User().save(model)

    return render_template(WebPaths.get_admin_path("user/user_list_save.html"), model=model, err=err)


@admin_blue.route('user_list_del', methods=['GET', 'POST'])
def user_list_del():
    User().delete_from_page(http_helper.get_prams("ids"))
    return redirect("user_list")

# endregion
