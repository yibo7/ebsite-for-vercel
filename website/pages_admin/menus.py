from flask import render_template, request, redirect

from entity.admin_menus_model import AdminMenuModel
from website.pages_admin import admin_blue
from eb_utils import http_helper
from eb_utils.configs import WebPaths
from bll.admin_menus import AdminMenus


@admin_blue.route('menus', methods=['GET'])
def admin_menus():
    datas = AdminMenus().get_tree()
    pager = ''
    keyword = http_helper.get_prams("k")
    if keyword:
        page_num = http_helper.get_prams_int("p", 1)
        datas, pager = AdminMenus().search(keyword, page_num, 'menu_name')
    return render_template(WebPaths.get_admin_path("menus/list.html"), pager=pager, datas=datas)


@admin_blue.route('menus_save', methods=['GET', 'POST'])
def admin_menus_save():
    model = AdminMenuModel()
    # print(model.is_menu)
    bll = AdminMenus()
    modify_id = http_helper.get_prams("_id")
    if modify_id:
        model = bll.find_one_by_id(modify_id)
    if request.method == 'POST':
        dic_prams = http_helper.get_prams_dict()
        model.dict_to_model(dic_prams)
        _id = bll.save(model)
        return redirect("menus")
    p_data = bll.get_tree_text()
    return render_template(WebPaths.get_admin_path("menus/save.html"), model=model, p_data=p_data)


@admin_blue.route('menus_resetorderid', methods=['GET', 'POST'])
def menus_resetorderid():
    AdminMenus().reset_orderid()
    return redirect("menus")


@admin_blue.route('menus_del', methods=['GET', 'POST'])
def menus_del():
    AdminMenus().delete_from_page(http_helper.get_prams("ids"))
    return redirect("menus")


@admin_blue.route('menus_move', methods=['GET', 'POST'])
def menus_move():
    if request.method == 'POST':
        from_id = http_helper.get_prams("from_id")
        target_id = http_helper.get_prams("target_id")
        i_move_type = http_helper.get_prams_int("mt")
        AdminMenus().move_to(from_id, target_id, i_move_type)
        return redirect("menus_move")

    datas = AdminMenus().get_tree_text()
    return render_template(WebPaths.get_admin_path("menus/move.html"), datas=datas)
