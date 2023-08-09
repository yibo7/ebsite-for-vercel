from flask import render_template, request, redirect, g

from bll.new_class import NewsClass
from bll.new_content import NewsContent
from bll.templates import Templates
from bll.user_group import UserGroup
from entity.news_content_model import NewsContentModel
from entity.templates_model import TemplatesModel
from entity.user_group_model import UserGroupModel
from entity.user_token import UserToken
from temp_expand import get_table_html
from website.pages_admin import admin_blue
from eb_utils import http_helper
from eb_utils.configs import WebPaths


# region class

@admin_blue.route('content_list', methods=['GET'])
def content_list():
    keyword = http_helper.get_prams("k")
    page_num = http_helper.get_prams_int("p", 1)
    bll = NewsContent()
    datas, pager = bll.search(keyword, page_num, 'title')

    del_btn = {"show_name": "删除", "url": "content_list_del?ids=#_id#", "confirm": True}
    modify_btn = {"show_name": "修改", "url": "content_list_save?_id=#_id#", "confirm": False}

    table_html = get_table_html(datas, [del_btn, modify_btn])

    return render_template(WebPaths.get_admin_path("news_content/content_list.html"), table_html=table_html, pager=pager)


@admin_blue.route('content_list_save', methods=['GET', 'POST'])
def content_list_save():
    g_id = http_helper.get_prams('_id')
    model = NewsContentModel()
    bll = NewsContent()
    if g_id:
        model = bll.find_one_by_id(g_id)
    err = ''
    if request.method == 'POST':
        admin_token: UserToken = g.u
        dic_prams = http_helper.get_prams_dict()
        model.dict_to_model(dic_prams)
        model.user_id = admin_token.id
        model.user_name = admin_token.name
        model.user_ni_name = admin_token.ni_name

        class_model = NewsClass().find_one_by_id(model.class_id)
        model.content_temp_id = class_model.content_temp_id
        model.class_nane = class_model.class_name

        bll.save(model)
        return redirect('content_list')

    class_list = NewsClass().get_tree_text()

    return render_template(WebPaths.get_admin_path("news_content/content_list_save.html"),class_list=class_list, model=model, err=err)


@admin_blue.route('content_list_del', methods=['GET', 'POST'])
def content_list_del():
    UserGroup().delete_from_page(http_helper.get_prams("ids"))
    return redirect("content_list")


# endregion

# region template

@admin_blue.route('content_temp_list', methods=['GET'])
def content_temp_list():
    tp = Templates(2)
    datas = tp.get_templates()

    del_btn = {"show_name": "删除", "url": "content_temp_list_del?ids=#_id#", "confirm": True}
    modify_btn = {"show_name": "修改", "url": "content_temp_list_save?_id=#_id#", "confirm": False}

    table_html = get_table_html(datas, [del_btn, modify_btn])

    return render_template(WebPaths.get_admin_path("news_content/content_temp_list.html"), table_html=table_html)


@admin_blue.route('content_temp_list_save', methods=['GET', 'POST'])
def content_temp_list_save():
    g_id = http_helper.get_prams('_id')
    model = TemplatesModel()
    bll = Templates(2)
    model.temp_type = bll.temp_type
    if g_id:
        model = bll.find_one_by_id(g_id)
    err = ''
    if request.method == 'POST':
        dic_prams = http_helper.get_prams_dict()
        model.dict_to_model(dic_prams)
        bll.save(model)
        return redirect('content_temp_list')

    return render_template(WebPaths.get_admin_path("news_content/content_temp_list_save.html"), model=model, err=err)


@admin_blue.route('content_temp_list_del', methods=['GET', 'POST'])
def content_temp_list_del():
    UserGroup().delete_from_page(http_helper.get_prams("ids"))
    return redirect("content_temp_list")


# endregion

