from flask import render_template, request, redirect, g

from bll.widgets import Widgets
from entity.widgets_model import WidgetsModel
from temp_expand import get_table_html
from website.pages_admin import admin_blue
from eb_utils import http_helper, get_all_fields
from eb_utils.configs import WebPaths


# region class

@admin_blue.route('widget_list', methods=['GET'])
def widgets_list():
    keyword = http_helper.get_prams("k")
    page_num = http_helper.get_prams_int("p", 1)
    datas, pager = Widgets().search(keyword, page_num, 'name')

    del_btn = {"show_name": "删除", "url": "widget_list_del?ids=#_id#", "confirm": True}
    modify_btn = {"show_name": "修改", "url": "widget_list_save?_id=#_id#", "confirm": False}
    open_code_btn = {"show_name": "调用代码", "url": "javascript:open_code('#_id#')", "confirm": False}

    table_html = get_table_html(datas, [del_btn, modify_btn, open_code_btn])

    return render_template(WebPaths.get_admin_path("widgets/widget_list.html"), pager=pager,
                           table_html=table_html)


@admin_blue.route('widget_sel_type', methods=['GET'])
def widget_sel_type():
    data_list = Widgets().get_types()
    return render_template(WebPaths.get_admin_path("widgets/widget_sel_type.html"), data_list=data_list)


@admin_blue.route('widget_list_save', methods=['GET', 'POST'])
def widgets_list_save():
    g_id = http_helper.get_prams('_id')
    temp_type = http_helper.get_prams_int('t')
    model = WidgetsModel()
    model.temp_type = temp_type
    bll = Widgets()
    if g_id:
        model = bll.find_one_by_id(g_id)
    err = ''
    if request.method == 'POST':
        dic_prams = http_helper.get_prams_dict()
        model.dict_to_model(dic_prams)
        model.user_id = g.uid
        bll.save(model)
        return redirect('widget_list')

    all_fields = ''

    temp_file = 'widget_list_save_where.html'
    if model.temp_type == 5:
        temp_file = 'widget_list_save_text.html'
    elif model.temp_type == 6:
        temp_file = 'widget_list_save_html.html'
    else:
        temp_type = bll.get_type_by_id(model.temp_type)
        all_fields = get_all_fields(temp_type.get('bll').new_instance())
    desc_asc = bll.get_desc_asc()



    return render_template(WebPaths.get_admin_path(f"widgets/{temp_file}"),all_fields=all_fields, desc_asc=desc_asc, model=model, err=err)


@admin_blue.route('widget_list_del', methods=['GET', 'POST'])
def widgets_list_del():
    Widgets().delete_from_page(http_helper.get_prams("ids"))
    return redirect("widget_list")

# endregion
