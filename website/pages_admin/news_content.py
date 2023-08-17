from flask import render_template, request, redirect, g, render_template_string

from bll.new_class import NewsClass
from bll.new_content import NewsContent

from bll.site_model import SiteModel
from entity.news_content_model import NewsContentModel
from entity.site_model_entity import FieldModel
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
    datas, pager = bll.search_content(keyword, class_id, page_num)

    del_btn = {"show_name": "删除", "url": "content_list_del?ids=#_id#", "confirm": True}
    modify_btn = {"show_name": "修改", "url": "content_list_save?_id=#_id#", "confirm": False}

    table_html = get_table_html(datas, [del_btn, modify_btn])
    class_list = NewsClass().get_tree_text()
    return render_template(WebPaths.get_admin_path("news_content/content_list.html"), table_html=table_html,
                           pager=pager, class_id=class_id, class_list=class_list)


@admin_blue.route('content_list_save', methods=['GET', 'POST'])
def content_list_save():
    g_id = http_helper.get_prams('_id')
    bll = NewsContent()
    model = bll.new_instance()

    if g_id:
        model = bll.find_one_by_id(g_id)
        class_id = model.class_id
    else:
        class_id = request.args.get('cid')

    class_model = NewsClass().find_one_by_id(class_id)

    err = ''
    if request.method == 'POST':
        admin_token: UserToken = g.u
        dic_prams = http_helper.get_prams_dict()
        model.dict_to_model(dic_prams)
        model.user_id = admin_token.id
        model.user_name = admin_token.name
        model.user_ni_name = admin_token.ni_name

        # class_model = NewsClass().find_one_by_id(model.class_id)
        model.class_name = class_model.class_name
        model.class_id = class_id
        bll.save(model)
        return redirect('content_list')

    # class_list = NewsClass().get_tree_text()
    class_name = class_model.class_name
    model_html_temp = SiteModel().get_model_temp_by_id(class_model.content_model_id)
    model_html = render_template_string(model_html_temp,model=model)
    return render_template(WebPaths.get_admin_path("news_content/content_list_save.html"),
                           model=model, err=err,class_name=class_name, model_html=model_html)


@admin_blue.route('content_list_del', methods=['GET', 'POST'])
def content_list_del():
    NewsContent().delete_from_page(http_helper.get_prams("ids"))
    return redirect("content_list")


# endregion

# region content model


@admin_blue.route('content_model_list', methods=['GET'])
def content_model_list():
    bll = SiteModel()
    datas = bll.find_all()

    del_btn = {"show_name": "删除", "url": f"content_model_list_del?ids=#_id#", "confirm": True}
    modify_btn = {"show_name": "修改", "url": f"content_model_list_save?_id=#_id#", "confirm": False}
    fields_btn = {"show_name": "管理字段", "url": f"content_model_fields?_id=#_id#", "confirm": False}

    table_html = get_table_html(datas, [del_btn, modify_btn, fields_btn], False)

    return render_template(WebPaths.get_admin_path("news_content/content_model_list.html"), table_html=table_html)


@admin_blue.route('content_model_list_save', methods=['GET', 'POST'])
def content_model_list_save():
    g_id = http_helper.get_prams('_id')

    bll = SiteModel()
    model = bll.new_instance()
    if g_id:
        model = bll.find_one_by_id(g_id)
    err = ''
    if request.method == 'POST':
        model.name = http_helper.get_prams('name')
        bll.save_default(model)
        return redirect('content_model_list')

    return render_template(WebPaths.get_admin_path("news_content/content_model_list_save.html"), model=model, err=err)


@admin_blue.route('content_model_list_del', methods=['GET', 'POST'])
def content_model_list_del():
    SiteModel().delete_from_page(http_helper.get_prams("ids"))
    return redirect(f"content_model_list")


@admin_blue.route('content_model_fields', methods=['GET', 'POST'])
def content_model_fields():
    g_id = request.args.get('_id')

    bll = SiteModel()
    model = bll.find_one_by_id(g_id)
    err = ''
    if request.method == 'POST':
        dict_prams = http_helper.get_prams_dict()

        ctr_id = dict_prams.get('control_id')
        control = bll.get_control_by_id(int(ctr_id))
        dict_prams['control_name'] = control.name
        field_model = FieldModel(**dict_prams)
        is_ok = bll.save_fields(model, field_model)
        if not is_ok:
            err = '已经存在相同的字段，若想修改请删除后再添加'
    fields = bll.get_fields()
    controls = bll.get_controls()

    return render_template(WebPaths.get_admin_path("news_content/content_model_fields.html"), model=model,
                           controls=controls, fields=fields, err=err)


@admin_blue.route('content_model_fields_del', methods=['GET', 'POST'])
def content_model_fields_del():
    _id = http_helper.get_prams('_id')
    field_name = http_helper.get_prams('field_name')
    SiteModel().del_field(_id,field_name)
    return redirect(f"content_model_fields?_id={_id}")
# endregion
