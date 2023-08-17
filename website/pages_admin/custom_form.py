from flask import render_template, request, redirect

from bll.custom_form import CustomForm
from bll.custom_form_data import CustomFormData
from eb_utils.mvc_pager import pager_html_admin
from entity.custom_form_model import CustomFormModel
from temp_expand import get_table_html
from website.pages_admin import admin_blue
from eb_utils import http_helper
from eb_utils.configs import WebPaths, SiteConstant


# region custom form

@admin_blue.route('form_list', methods=['GET'])
def form_list():
    bll = CustomForm()
    data_list = bll.find_all()
    del_btn = {"show_name": "删除", "url": "form_list_del?ids=#_id#", "confirm": True}
    modify_btn = {"show_name": "修改", "url": "form_list_save?_id=#_id#", "confirm": False}
    fields_btn = {"show_name": "管理字段", "url": f"form_field_list?_id=#_id#", "confirm": False}
    showdata_btn = {"show_name": "查看数据", "url": "form_data_list?_id=#_id#", "confirm": False}

    table_html = get_table_html(data_list, [del_btn, modify_btn, fields_btn, showdata_btn])
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
        model.open_safe_code = http_helper.get_prams_bool('open_safe_code')
        model.max_len = http_helper.get_prams_int('max_len')
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


# endregion

# region form field

@admin_blue.route('form_field_list', methods=['GET', 'POST'])
def form_field_list():
    g_id = request.args.get('_id')

    bll = CustomForm()
    model = bll.find_one_by_id(g_id)
    err = ''
    if request.method == 'POST':
        dict_prams = http_helper.get_prams_dict()
        is_ok = bll.save_fields(model, dict_prams)
        if not is_ok:
            err = '已经存在相同的字段，若想修改请删除后再添加'

    demo_tem = bll.get_demo_tem(model)

    return render_template(WebPaths.get_admin_path("custom_form/form_field_list.html"), model=model,demo_tem=demo_tem, err=err)


@admin_blue.route('form_field_list_del', methods=['GET', 'POST'])
def form_field_list_del():
    _id = http_helper.get_prams('_id')
    field_name = http_helper.get_prams('field_name')
    CustomForm().del_field(_id, field_name)
    return redirect(f"form_field_list?_id={_id}")


# endregion

# region form data

@admin_blue.route('form_data_list', methods=['GET', 'POST'])
def form_data_list():
    g_id = request.args.get('_id')
    bll_form = CustomForm()
    model = bll_form.find_one_by_id(g_id)
    err = ''
    bll_form_data = CustomFormData()
    page_number = http_helper.get_prams_int("p", 1)
    page_size = SiteConstant.PAGE_SIZE_AD
    i_count, data_list = bll_form_data.find_pages(page_number, page_size, model)

    pager = pager_html_admin(i_count, page_number, page_size, {'_id': g_id})

    return render_template(WebPaths.get_admin_path("custom_form/form_data_list.html"), model=model, data_list=data_list,
                           pager=pager, err=err)


@admin_blue.route('form_data_list_del', methods=['GET', 'POST'])
def form_data_list_del():
    ids = http_helper.get_prams('ids')
    CustomFormData().delete_from_page(ids)
    form_id = http_helper.get_prams('form_id')
    return redirect(f"form_data_list?_id={form_id}")

# endregion