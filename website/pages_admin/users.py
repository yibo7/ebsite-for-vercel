from flask import render_template, request, redirect

from website.pages_admin import admin_blue
from eb_utils import http_helper, update_dic_to_dic,  get_table_html
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

    cols = {
        # "_id": "ID",
        "username": "账号",
        "ni_name": "昵称",
        'group_id|to_user_group_name': '用户组',
        "mobile_number": "手机号",
        'email_address': '邮箱地址',
        'is_locked|to_bool_name': '是否锁定',
        'credits': '积分',
        'last_login_date': '最后登录时间',
        'last_login_ip': '最后登录IP',
        'login_count': '登录次数',
        'reg_remark': '备注',
        'id': 'ID序号',
        '_id': 'ID',
        "add_time": "添加时间"
    }
    del_btn = {"show_name": "删除", "url": "user_list_del?ids=#_id#", "confirm": True}
    modify_btn = {"show_name": "修改", "url": "user_list_save?id=#_id#", "confirm": False}

    table_html = get_table_html(datas, cols, [del_btn, modify_btn])

    return render_template(WebPaths.get_admin_path("user/user_list.html"), table_html=table_html, pager=pager, datas=datas)


@admin_blue.route('user_list_save', methods=['GET', 'POST'])
def user_list_save():
    data_id = http_helper.get_prams('id')
    model = User().__dict__
    if data_id:
        model = User().find_one_by_id(data_id)

    err = ''
    if request.method == 'POST':
        dic_prams = http_helper.get_prams_dict()
        update_dic_to_dic(dic_prams, model)
        _id = User().save(model)
        return redirect('user_list')
    group = UserGroup().find_all()
    return render_template(WebPaths.get_admin_path("user/user_list_save.html"), model=model, group=group, err=err)


@admin_blue.route('user_list_del', methods=['GET', 'POST'])
def user_list_del():
    User().delete_from_page(http_helper.get_prams("ids"))
    return redirect("user_list")

# endregion
