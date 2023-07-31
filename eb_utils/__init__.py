from dataclasses import replace

from flask import render_template_string, current_app
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


def get_table_html(data_source, btn_actions=None, show_selbox: bool = True):
    # region get tr_items
    tr_items = []
    cols = []
    for item in data_source:

        tr_item = []
        int_id_value = ""
        g_id_value = ""
        filter_name = ''

        if hasattr(item, 'id'):
            int_id_value = item.id
        if hasattr(item, '_id'):
            g_id_value = item._id

        # titles = item.get_titles()
        for title in item.get_titles():
            tr_item.append(title.get('value'))
            cols.append(title.get('title'))

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
    # endregion

    if btn_actions:
        cols.append("操作")

    temp_html = """
        <table class="table table-hover eb-table">
            <thead>
                <tr>
                    {% for value in cols %}
                        <th scope="col">{{ value }}</th>
                    {% endfor %}
                    {% if show_selbox %}
                        <th scope='col'><input id='chAll' onclick='on_check(this)' type='checkbox' /></th>
                    {% endif %}
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
    t_html = render_template_string(temp_html, cols=cols, tr_items=tr_items, show_selbox=show_selbox)
    return Markup(t_html)
