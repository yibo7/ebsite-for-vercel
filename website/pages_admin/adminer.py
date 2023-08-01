from flask import render_template, request, redirect, jsonify, g

from bll.admin_menus import AdminMenus
from bll.admin_role import AdminRole
from bll.admin_user import AdminUser
from entity.admin_role_model import AdminRoleModel
from entity.admin_user_model import AdminUserModel
from entity.api_msg import ApiMsg
from temp_expand import get_table_html
from website.pages_admin import admin_blue
from eb_utils import http_helper
from eb_utils.configs import WebPaths


# region admin-role

@admin_blue.route('admin_roles', methods=['GET'])
def admin_role():
    bll = AdminRole()

    data_list = bll.find_all()

    del_btn = {"show_name": "删除", "url": "admin_roles_del?ids=#_id#", "confirm": True}
    modify_btn = {"show_name": "修改", "url": "admin_roles_save?_id=#_id#", "confirm": False}
    # WebPaths.ADMIN_PATH
    pos_btn = {"show_name": "分配权限", "url": "javascript:OpenIframe('adminer_roles_pos?rid=#_id#','分配权限')",
               "confirm": False}

    table_html = get_table_html(data_list, [del_btn, modify_btn, pos_btn])

    return render_template(WebPaths.get_admin_path("adminer/adminer_roles.html"), table_html=table_html,
                           datas=data_list)


@admin_blue.route('admin_roles_save', methods=['GET', 'POST'])
def admin_role_save():
    g_id = http_helper.get_prams('_id')
    model = AdminRoleModel()
    bll = AdminRole()
    if g_id:
        model = bll.find_one_by_id(g_id)
    err = ''
    if request.method == 'POST':
        dic_prams = http_helper.get_prams_dict()
        model.dict_to_model(dic_prams)
        bll.save(model)
        return redirect('admin_roles')

    return render_template(WebPaths.get_admin_path("adminer/adminer_role_save.html"), model=model, err=err)


@admin_blue.route('admin_roles_del', methods=['GET', 'POST'])
def admin_role_del():
    AdminRole().delete_from_page(http_helper.get_prams("ids"))
    return redirect("admin_roles")


@admin_blue.route('adminer_roles_pos', methods=['GET', 'POST'])
def adminer_roles_pos():
    role_id = http_helper.get_prams('rid')
    bll = AdminRole()
    if request.method == 'POST':
        api_msg = ApiMsg('权限分配成功')

        pos_ids = http_helper.get_prams('pmsids')
        try:
            bll.add_pos(role_id, pos_ids)
            api_msg.success = True
        except Exception as e:
            api_msg.data = f'添加失败：{e}'

        return jsonify(api_msg.__dict__)
    data_list = AdminMenus().get_tree()
    model = bll.find_one_by_id(role_id)
    table_html = get_table_html(data_list,None,True,model.pos_id)

    return render_template(WebPaths.get_admin_path("adminer/adminer_roles_pos.html"), table_html=table_html)


# endregion

# region admins


@admin_blue.route('admin_list', methods=['GET'])
def admin_list():
    keyword = http_helper.get_prams("k")
    page_num = http_helper.get_prams_int("p", 1)
    bll = AdminUser()
    datas, pager = bll.search(keyword, page_num, 'user_name')

    del_btn = {"show_name": "删除", "url": "admin_list_del?ids=#_id#", "confirm": True}
    modify_btn = {"show_name": "修改", "url": "admin_list_save?_id=#_id#", "confirm": False}

    table_html = get_table_html(datas, [del_btn, modify_btn])

    return render_template(WebPaths.get_admin_path("adminer/admin_list.html"), table_html=table_html, pager=pager,
                           datas=datas)


@admin_blue.route('admin_list_save', methods=['GET', 'POST'])
def admin_list_save():
    data_id = http_helper.get_prams('_id')
    model = AdminUserModel()
    bll = AdminUser()
    if data_id:
        model = bll.find_one_by_id(data_id)

    err = ''
    if request.method == 'POST':
        dic_prams = http_helper.get_prams_dict()
        model.dict_to_model(dic_prams)
        if data_id:
            is_success = bll.update(model)
        else:
            is_success, err = bll.reg_user(model)
        if is_success:
            return redirect('admin_list')

    role = AdminRole().find_all()

    return render_template(WebPaths.get_admin_path("adminer/admin_list_save.html"), role=role, model=model, err=err)


@admin_blue.route('admin_list_del', methods=['GET', 'POST'])
def admin_list_del():
    AdminUser().delete_from_page(http_helper.get_prams("ids"))
    return redirect("admin_list")


@admin_blue.route('admin_change_pass', methods=['GET', 'POST'])
def admin_change_pass():
    err = ''
    if request.method == 'POST':
        bll = AdminUser()
        dic_prams = http_helper.get_prams_dict()
        model = bll.find_one_by_id(g.uid)
        is_success, err = bll.change_pass(dic_prams.get('old_pass'), dic_prams.get('new_pass'), dic_prams.get('re_new_pass'),model)
    return render_template(WebPaths.get_admin_path("adminer/admin_change_pass.html"), err=err)
# endregion
