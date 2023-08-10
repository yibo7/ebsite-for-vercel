from flask import render_template, request, redirect, g

from bll.new_class import NewsClass
from bll.new_content import NewsContent
from bll.site_model_bll import SiteModelBll
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


# region content

@admin_blue.route('content_list', methods=['GET'])
def content_list():
    keyword = http_helper.get_prams("k")
    page_num = http_helper.get_prams_int("p", 1)
    class_id = http_helper.get_prams("cid")
    bll = NewsContent()
    datas, pager = bll.search_content(keyword,class_id, page_num)

    del_btn = {"show_name": "删除", "url": "content_list_del?ids=#_id#", "confirm": True}
    modify_btn = {"show_name": "修改", "url": "content_list_save?_id=#_id#", "confirm": False}

    table_html = get_table_html(datas, [del_btn, modify_btn])
    class_list = NewsClass().get_tree_text()
    return render_template(WebPaths.get_admin_path("news_content/content_list.html"), table_html=table_html, pager=pager, class_id=class_id, class_list=class_list)


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
        # model.content_temp_id = class_model.content_temp_id
        model.class_name = class_model.class_name

        bll.save(model)
        return redirect('content_list')

    class_list = NewsClass().get_tree_text()

    return render_template(WebPaths.get_admin_path("news_content/content_list_save.html"),class_list=class_list, model=model, err=err)


@admin_blue.route('content_list_del', methods=['GET', 'POST'])
def content_list_del():
    NewsContent().delete_from_page(http_helper.get_prams("ids"))
    return redirect("content_list")


# endregion

# region content model


@admin_blue.route('content_model_list', methods=['GET'])
def content_model_list():
    bll = SiteModelBll()
    datas = bll.find_all()

    del_btn = {"show_name": "删除", "url": f"content_model_list_del?ids=#_id#", "confirm": True}
    modify_btn = {"show_name": "修改", "url": f"content_model_list_save?_id=#_id#", "confirm": False}

    table_html = get_table_html(datas, [del_btn, modify_btn])

    return render_template(WebPaths.get_admin_path("news_content/content_model_list.html"), table_html=table_html)


@admin_blue.route('content_model_list_save', methods=['GET', 'POST'])
def content_model_list_save():
    g_id = http_helper.get_prams('_id')

    bll = SiteModelBll()
    model = bll.new_instance()
    if g_id:
        model = bll.find_one_by_id(g_id)
    err = ''
    if request.method == 'POST':
        dic_prams = http_helper.get_prams_dict()
        model.dict_to_model(dic_prams)
        bll.save(model)
        return redirect('content_model_list')

    return render_template(WebPaths.get_admin_path("news_content/content_model_list_save.html"), model=model, err=err)


@admin_blue.route('content_model_list_del', methods=['GET', 'POST'])
def content_model_list_del():
    SiteModelBll().delete_from_page(http_helper.get_prams("ids"))
    return redirect(f"content_model_list")

# endregion


