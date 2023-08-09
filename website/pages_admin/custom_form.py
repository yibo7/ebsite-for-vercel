from flask import render_template, request, redirect

from bll.custom_form import CustomForm
from entity.custom_form_model import CustomFormModel
from temp_expand import get_table_html
from website.pages_admin import admin_blue
from eb_utils import http_helper
from eb_utils.configs import WebPaths


# region class

@admin_blue.route('form_list', methods=['GET'])
def form_list():
    bll = CustomForm()
    data_list = bll.find_all()
    del_btn = {"show_name": "删除", "url": "form_list_del?ids=#_id#", "confirm": True}
    modify_btn = {"show_name": "修改", "url": "form_list_save?_id=#_id#", "confirm": False}
    field_btn = {"show_name": "查看数据", "url": "form_field_list?_id=#_id#", "confirm": False}

    table_html = get_table_html(data_list, [del_btn, modify_btn, field_btn])
    return render_template(WebPaths.get_admin_path("custom_form/form_list.html"), table_html=table_html)


@admin_blue.route('form_list_save', methods=['GET', 'POST'])
def form_list_save():
    g_id = http_helper.get_prams('_id')
    model = CustomFormModel()
    bll = CustomForm()
    if g_id:
        model = bll.find_one_by_id(g_id)
    err = ''
    if request.method == 'POST':
        name = http_helper.get_prams('name')
        model.name = name

        model.form_fields = http_helper.get_prams('form_fields')

        if not g_id and bll.exist_data('name', name):
            err = '已经存在相同的表单名称'
        else:
            bll.save(model)
            return redirect('form_list')

    return render_template(WebPaths.get_admin_path("custom_form/form_list_save.html"), model=model, err=err)


@admin_blue.route('form_list_del', methods=['GET', 'POST'])
def form_list_del():
    CustomForm().delete_from_page(http_helper.get_prams("ids"))
    return redirect("form_list")


@admin_blue.route('form_field_list', methods=['GET'])
def form_field_list():
    bll = CustomForm()
    return render_template(WebPaths.get_admin_path("custom_form/form_field_list.html"))

# endregion
