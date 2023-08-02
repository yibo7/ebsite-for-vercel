from flask import render_template, request, redirect, jsonify, g

from bll.admin_login_log import AdminLoginLog
from bll.admin_user import AdminUser
from bll.site_log import SiteLog
from temp_expand import get_table_html
from website.pages_admin import admin_blue
from eb_utils import http_helper
from eb_utils.configs import WebPaths


# region admin login log


@admin_blue.route('admin_login_log_list', methods=['GET'])
def admin_login_log_list():
    keyword = http_helper.get_prams("k")
    page_num = http_helper.get_prams_int("p", 1)
    bll = AdminLoginLog()
    data_list, pager = bll.search(keyword, page_num, 'title')

    del_btn = {"show_name": "删除", "url": "admin_login_log_list_del?ids=#_id#", "confirm": True}
    # modify_btn = {"show_name": "修改", "url": "admin_list_save?_id=#_id#", "confirm": False}

    table_html = get_table_html(data_list, [del_btn])

    return render_template(WebPaths.get_admin_path("log/admin_login_log_list.html"), table_html=table_html,
                           pager=pager,
                           datas=data_list)


@admin_blue.route('admin_login_log_list_del', methods=['GET', 'POST'])
def admin_login_log_list_del():
    AdminLoginLog().delete_from_page(http_helper.get_prams("ids"))
    return redirect("admin_login_log_list")

# endregion

# region site log


@admin_blue.route('site_log_list', methods=['GET'])
def site_log_list():
    keyword = http_helper.get_prams("k")
    page_num = http_helper.get_prams_int("p", 1)
    bll = SiteLog()
    data_list, pager = bll.search(keyword, page_num, 'title')

    del_btn = {"show_name": "删除", "url": "site_log_list_del?ids=#_id#", "confirm": True}
    # modify_btn = {"show_name": "修改", "url": "admin_list_save?_id=#_id#", "confirm": False}

    table_html = get_table_html(data_list, [del_btn])

    return render_template(WebPaths.get_admin_path("log/site_log_list.html"), table_html=table_html,
                           pager=pager,
                           datas=data_list)


@admin_blue.route('site_log_list_del', methods=['GET', 'POST'])
def site_log_list_del():
    SiteLog().delete_from_page(http_helper.get_prams("ids"))
    return redirect("site_log_list")

# endregion
