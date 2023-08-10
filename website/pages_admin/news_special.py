from flask import render_template, request, redirect, g

from bll.new_content import NewsContent
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

    return render_template(WebPaths.get_admin_path("news_special/special_list.html"), pager=pager,
                           table_html=table_html)


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
    return render_template(WebPaths.get_admin_path("news_special/special_list_save.html"), p_list=p_list,
                           temp_special=temp_special, model=model, err=err)


@admin_blue.route('special_list_del', methods=['GET', 'POST'])
def special_list_del():
    NewsSpecial().delete_from_page(http_helper.get_prams("ids"))
    return redirect("special_list")


@admin_blue.route('special_sel_box', methods=['GET', 'POST'])
def special_sel_box():
    bll = NewsSpecial()
    ids = request.args.get('ids').split(',')
    if 'on' in ids:
        ids.remove('on')
    err = f'你正准备将{len(ids)}条数据添加到专题'
    if request.method == 'POST':
        sel_ids = request.form.getlist('sel_id')
        if sel_ids:
            bll.save_content_to_special(ids, sel_ids)
            err = '保存成功'
        else:
            err = '保存失败，请选择专题，可多选'
    data_list = bll.get_tree_text()
    return render_template(WebPaths.get_admin_path("news_special/special_sel_box.html"), data_list=data_list, ids=ids,
                           err=err)


# endregion


@admin_blue.route('special_content_list', methods=['GET'])
def special_content_list():
    s_id = http_helper.get_prams('sid')
    page_num = http_helper.get_prams_int("p", 1)
    err = ''
    data_list, pager = NewsSpecial().get_by_speical_id(s_id, page_num)

    del_btn = {"show_name": "删除", "url": f"special_content_list_del?ids=#_id#&sid={s_id}", "confirm": True}

    table_html = get_table_html(data_list, [del_btn])

    return render_template(WebPaths.get_admin_path("news_special/special_content_list.html"), table_html=table_html,
                           pager=pager, err=err, s_id=s_id)


@admin_blue.route('special_content_list_del', methods=['GET', 'POST'])
def special_content_list_del():
    s_id = http_helper.get_prams('sid')
    NewsSpecial().del_content(s_id, http_helper.get_prams("ids"))
    return redirect(f"special_content_list?sid={s_id}")


@admin_blue.route('special_content_list_clear', methods=['GET', 'POST'])
def special_content_list_clear():
    s_id = http_helper.get_prams('sid')
    NewsSpecial().clear_content(s_id)
    return redirect(f"special_content_list?sid={s_id}")
