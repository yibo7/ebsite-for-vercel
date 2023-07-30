from dataclasses import replace

from flask import render_template_string
from markupsafe import Markup

from eb_utils import string_check


def __convert_to_number(value):
    if string_check.is_int(value):
        return int(value)
    elif string_check.is_decimal(value):
        return float(value)
    elif value == 'on':
        return True
    elif value == 'checkbox_unchecked':
        return False
    else:
        return value


def update_dic_to_class(dic_obj: {}, class_model):
    settings_dict = class_model.__dict__
    convert_dic = {key: __convert_to_number(value) for key, value in dic_obj.items()}
    settings_dict.update(convert_dic)
    settings_model_new = replace(class_model, **settings_dict)
    return settings_model_new


def update_dic_to_dic(dic_from: dict, dic_to: dict):
    convert_dic = {key: __convert_to_number(value) for key, value in dic_from.items()}
    dic_to.update(convert_dic)
    return dic_to


def get_table_html(data_source, cols, btn_actions=None, show_selbox: bool = True):
    tr_items = []
    for item in data_source:
        tr_item = []
        int_id_value = ""
        g_id_value = ""
        filter_name = ''
        if 'id' in item:
            int_id_value = item['id']
        if '_id' in item:
            g_id_value = item['_id']
        for key, value in cols.items():
            if '|' in key:
                a_key = key.split('|')
                key = a_key[0]
                filter_name = a_key[1]
            col_value = item[key]
            if filter_name:
                col_value = '{{"' + str(col_value) + '"|' + filter_name + '}}'
                filter_name = ''
            tr_item.append(col_value)

        opt_html = ""
        if btn_actions:
            for btn in btn_actions:
                cf = "onclick=\"return confirm('确认要执行吗？');\"" if btn["confirm"] else ""
                opt_html = f"{opt_html} <a href='{btn['url']}' {cf} class='btn btn-info btn-sm' >{btn['show_name']}</a>"

        if opt_html:
            opt_html = opt_html.replace("#id#", str(int_id_value))
            opt_html = opt_html.replace("#_id#", str(g_id_value))
            tr_item.append(opt_html)
        if show_selbox:
            tr_item.append(f'<input value="{g_id_value}" type="checkbox" />')

        tr_items.append(tr_item)

    if btn_actions:
        cols["opt"] = "操作"
    table_html = ['<table class="table table-hover eb-table"><thead><tr>']
    for value in cols.values():
        table_html.append(f'<th scope="col">{value}</th>')
    if show_selbox:
        table_html.append("<th scope='col'><input id='chAll' onclick='on_check(this)' type='checkbox' /></th>")
    table_html.append('</tr></thead><tbody>')

    for row in tr_items:
        table_html.append('<tr>')
        for col_v in row:
            table_html.append(f'<td>{col_v}</td>')

        table_html.append('</tr>')

    table_html.append('</tbody></table>')
    temp_html = """
        <table class="table table-hover eb-table">
            <thead>
                <tr>
                    {% for value in cols.values() %}
                        <th scope="col">{{ value }}</th>
                    {% endfor %}
                    <th scope='col'><input id='chAll' onclick='on_check(this)' type='checkbox' /></th>
                </tr>
            </thead>
            <tbody>
                {% for row in tr_items %}
                    <tr>
                        {% for col_v in row %}
                            <td>{{ col_v | safe }}</td>
                         {% endfor %}
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    """
    t_html = render_template_string(temp_html, cols=cols,tr_items=tr_items)
    # t_html = render_template_string(''.join(table_html))
    return Markup(t_html)


def get_table_data2(data_source, cols, btn_actions=None):
    datas = []
    for item in data_source:
        data = []
        idv = ""
        g_idv = ""
        for key, value in cols.items():
            # data[value] = getattr(item, key)
            v = getattr(item, key)
            data.append(v)
            if key.lower() == "id":
                idv = v
            if key.lower() == "_id":
                g_idv = v

        opt_html = ""
        if btn_actions:
            for btn in btn_actions:
                cf = "onclick=\"return confirm('确认要执行吗？');\"" if btn["confirm"] else ""
                opt_html = f"{opt_html} <a href='{btn['url']}' {cf} class='btn btn-primary btn-sm' >{btn['show_name']}</a>"

        if opt_html:
            opt_html = opt_html.replace("#id#", str(idv))
            opt_html = opt_html.replace("#_id#", g_idv)
            data.append(opt_html)
        datas.append(data)

    if btn_actions:
        cols["opt"] = "操作"

    return [cols, datas]
