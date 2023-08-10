from flask import render_template, request, redirect, g

from bll.new_special import NewsSpecial
from bll.templates import Templates
from entity.news_special_model import NewsSpecialModel
from entity.templates_model import TemplatesModel
from temp_expand import get_table_html
from website.pages_admin import admin_blue
from eb_utils import http_helper
from eb_utils.configs import WebPaths


# region class

@admin_blue.route('special_list', methods=['GET'])
def special_list():

    datas = NewsSpecial().get_tree()
    pager = ''
    keyword = http_helper.get_prams("k")
    if keyword:
        page_num = http_helper.get_prams_int("p", 1)
        datas, pager = NewsSpecial().search(keyword, page_num, 'name')

    del_btn = {"show_name": "删除", "url": "special_list_del?ids=#_id#", "confirm": True}
    modify_btn = {"show_name": "修改", "url": "special_list_save?_id=#_id#", "confirm": False}

    table_html = get_table_html(datas, [del_btn, modify_btn])

    return render_template(WebPaths.get_admin_path("news_special/special_list.html"), pager=pager, table_html=table_html)


@admin_blue.route('special_list_save', methods=['GET', 'POST'])
def special_list_save():
    g_id = http_helper.get_prams('_id')
    model = NewsSpecialModel()
    bll = NewsSpecial()
    if g_id:
        model = bll.find_one_by_id(g_id)
    err = ''
    if request.method == 'POST':
        dic_prams = http_helper.get_prams_dict()
        model.dict_to_model(dic_prams)
        model.user_id = g.uid
        if not g_id and bll.exist_data('name', model.name):
            err = '已经存在相同名称的专题'
        else:
            bll.save(model)
            return redirect('special_list')
    temp_special = Templates(3).get_templates()
    p_list = bll.get_tree_text()
    return render_template(WebPaths.get_admin_path("news_special/special_list_save.html"), p_list=p_list, temp_special=temp_special, model=model, err=err)


@admin_blue.route('special_list_del', methods=['GET', 'POST'])
def special_list_del():
    NewsSpecial().delete_from_page(http_helper.get_prams("ids"))
    return redirect("special_list")


# endregion

# region template

# @admin_blue.route('special_temp_list', methods=['GET'])
# def special_temp_list():
#     tp = Templates(3)
#     datas = tp.get_templates()
#
#     del_btn = {"show_name": "删除", "url": "special_temp_list_del?ids=#_id#", "confirm": True}
#     modify_btn = {"show_name": "修改", "url": "special_temp_list_save?_id=#_id#", "confirm": False}
#
#     table_html = get_table_html(datas, [del_btn, modify_btn])
#
#     return render_template(WebPaths.get_admin_path("news_special/special_temp_list.html"), table_html=table_html)
#
#
# @admin_blue.route('special_temp_list_save', methods=['GET', 'POST'])
# def special_temp_list_save():
#     g_id = http_helper.get_prams('_id')
#     model = TemplatesModel()
#     bll = Templates(3)
#     model.temp_type = bll.temp_type
#     if g_id:
#         model = bll.find_one_by_id(g_id)
#     err = ''
#     if request.method == 'POST':
#         dic_prams = http_helper.get_prams_dict()
#         model.dict_to_model(dic_prams)
#         bll.save(model)
#         return redirect('special_temp_list')
#
#     return render_template(WebPaths.get_admin_path("news_special/special_temp_list_save.html"), model=model, err=err)
#
#
# @admin_blue.route('special_temp_list_del', methods=['GET', 'POST'])
# def special_temp_list_del():
#     Templates(3).delete_from_page(http_helper.get_prams("ids"))
#     return redirect("special_temp_list")


# endregion

