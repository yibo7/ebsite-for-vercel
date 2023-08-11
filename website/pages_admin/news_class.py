import pymongo
from flask import render_template, request, redirect, g

from bll.new_class import NewsClass
from bll.site_model import SiteModel
from bll.templates import Templates
from entity.news_class_model import NewsClassModel
from entity.templates_model import TemplatesModel
from entity.user_group_model import UserGroupModel
from temp_expand import get_table_html
from website.pages_admin import admin_blue
from eb_utils import http_helper
from eb_utils.configs import WebPaths


# region class

@admin_blue.route('class_list', methods=['GET'])
def class_list():
    bll = NewsClass()
    data_list = bll.get_tree()
    del_btn = {"show_name": "删除", "url": "class_list_del?ids=#_id#", "confirm": True}
    modify_btn = {"show_name": "修改", "url": "class_list_save?_id=#_id#", "confirm": False}
    add_content_btn = {"show_name": "添加内容", "url": "content_list_save?cid=#_id#", "confirm": False}

    table_html = get_table_html(data_list, [del_btn, modify_btn,add_content_btn])

    return render_template(WebPaths.get_admin_path("news_class/class_list.html"), table_html=table_html)


@admin_blue.route('class_list_save', methods=['GET', 'POST'])
def class_list_save():
    g_id = http_helper.get_prams('_id')
    model = NewsClassModel()
    bll = NewsClass()
    if g_id:
        model = bll.find_one_by_id(g_id)
    err = ''
    if request.method == 'POST':
        dic_prams = http_helper.get_prams_dict()
        model.dict_to_model(dic_prams)
        model.user_id = g.uid
        bll.save(model)
        return redirect('class_list')
    p_class_list = bll.get_tree_text()
    temp_class = Templates(1).get_templates()
    temp_content = Templates(2).get_templates()
    model_content = SiteModel().find_all()
    return render_template(WebPaths.get_admin_path("news_class/class_list_save.html"), temp_class=temp_class,
                           temp_content=temp_content, p_class_list=p_class_list, model_content=model_content,
                           model=model, err=err)


@admin_blue.route('class_list_del', methods=['GET', 'POST'])
def class_list_del():
    NewsClass().delete_from_page(http_helper.get_prams("ids"))
    return redirect("class_list")


@admin_blue.route('class_move', methods=['GET', 'POST'])
def class_move():
    if request.method == 'POST':
        from_id = http_helper.get_prams("from_id")
        target_id = http_helper.get_prams("target_id")
        i_move_type = http_helper.get_prams_int("mt")
        NewsClass().move_to(from_id, target_id, i_move_type)
        return redirect("class_move")

    datas = NewsClass().get_tree_text()
    return render_template(WebPaths.get_admin_path("news_class/move.html"), datas=datas)


@admin_blue.route('class_reset_orderid', methods=['GET', 'POST'])
def class_reset_orderid():
    NewsClass().reset_orderid()
    return redirect("class_list")


# endregion

# region template
#
# @admin_blue.route('class_temp_list', methods=['GET'])
# def class_temp_list():
#     tp = Templates(1)
#     datas = tp.get_templates()
#
#     del_btn = {"show_name": "删除", "url": "class_temp_list_del?ids=#_id#", "confirm": True}
#     modify_btn = {"show_name": "修改", "url": "class_temp_list_save?_id=#_id#", "confirm": False}
#
#     table_html = get_table_html(datas, [del_btn, modify_btn])
#
#     return render_template(WebPaths.get_admin_path("news_class/class_temp_list.html"), table_html=table_html)
#
#
# @admin_blue.route('class_temp_list_save', methods=['GET', 'POST'])
# def class_temp_list_save():
#     g_id = http_helper.get_prams('_id')
#     model = TemplatesModel()
#     bll = Templates(1)
#     model.temp_type = bll.temp_type
#     if g_id:
#         model = bll.find_one_by_id(g_id)
#     err = ''
#     if request.method == 'POST':
#         dic_prams = http_helper.get_prams_dict()
#         model.dict_to_model(dic_prams)
#         bll.save(model)
#         return redirect('class_temp_list')
#
#     return render_template(WebPaths.get_admin_path("news_class/class_temp_list_save.html"), model=model, err=err)
#
#
# @admin_blue.route('class_temp_list_del', methods=['GET', 'POST'])
# def class_temp_list_del():
#     Templates(1).delete_from_page(http_helper.get_prams("ids"))
#     return redirect("class_temp_list")

# endregion
