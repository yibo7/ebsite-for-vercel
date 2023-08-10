from flask import render_template, request, redirect

from bll.templates import Templates
from entity.templates_model import TemplatesModel
from temp_expand import get_table_html
from website.pages_admin import admin_blue
from eb_utils import http_helper
from eb_utils.configs import WebPaths


@admin_blue.route('temp_list', methods=['GET'])
def temp_list():
    temp_t = http_helper.get_prams_int('t')
    tp = Templates(temp_t)
    datas = tp.get_templates()

    del_btn = {"show_name": "删除", "url": f"temp_list_del?t={temp_t}&ids=#_id#", "confirm": True}
    modify_btn = {"show_name": "修改", "url": f"temp_list_save?t={temp_t}&_id=#_id#", "confirm": False}

    table_html = get_table_html(datas, [del_btn, modify_btn])

    return render_template(WebPaths.get_admin_path("templates/temp_list.html"), temp_t=temp_t, table_html=table_html)


@admin_blue.route('temp_list_save', methods=['GET', 'POST'])
def temp_list_save():
    temp_t = request.args.get('t', type=int, default=0)
    g_id = http_helper.get_prams('_id')

    bll = Templates(temp_t)
    model = bll.new_instance()
    model.temp_type = bll.temp_type
    if g_id:
        model = bll.find_one_by_id(g_id)
    err = ''
    if request.method == 'POST':
        dic_prams = http_helper.get_prams_dict()
        model.dict_to_model(dic_prams)
        bll.save(model)
        return redirect(f'temp_list?t={temp_t}')

    return render_template(WebPaths.get_admin_path("templates/temp_list_save.html"), model=model, err=err)


@admin_blue.route('temp_list_del', methods=['GET', 'POST'])
def temp_list_del():
    temp_t = http_helper.get_prams_int('t')
    Templates(temp_t).delete_from_page(http_helper.get_prams("ids"))
    return redirect(f"temp_list?t={temp_t}")


