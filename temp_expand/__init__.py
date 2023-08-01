from flask import render_template_string
from markupsafe import Markup

from temp_expand.template_filter import reg_temp_expand_filter
from temp_expand.template_fun import reg_temp_expand_fun


# import temp_expand
# def reg_temp_expand_filter(app):
#     for name in dir(temp_expand):
#         obj = getattr(temp_expand, name)
#         if callable(obj) and name.endswith('_filter'):
#             app.add_template_filter(obj)

def reg_temp_expand(app):
    reg_temp_expand_filter(app)
    reg_temp_expand_fun(app)


def get_table_html(data_source, btn_actions=None, show_selbox: bool = True, sel_id=[]):
    # region get tr_items
    tr_items = []
    header_cols = []
    is_header_init = False
    for item in data_source:

        tr_item = []
        int_id_value = ""
        g_id_value = ""

        if hasattr(item, 'id'):
            int_id_value = item.id
        if hasattr(item, '_id'):
            g_id_value = item._id

        for title in item.get_titles():
            tr_item.append(title.get('value'))
            if not is_header_init:
                header_cols.append(title.get('title'))

        is_header_init = True

        opt_html = ""
        if btn_actions:
            for btn in btn_actions:
                cf = "onclick=\"return confirm('确认要执行吗？');\"" if btn["confirm"] else ""
                opt_html = f"{opt_html} <a href=\"{btn['url']}\" {cf} class='btn btn-info btn-sm' >{btn['show_name']}</a>"

        if opt_html:
            opt_html = opt_html.replace("#id#", str(int_id_value))
            opt_html = opt_html.replace("#_id#", str(g_id_value))
            tr_item.append(opt_html)
        if show_selbox:
            check_tag = ''
            if str(g_id_value) in sel_id:
                check_tag = 'checked'
            tr_item.append(f'<input value="{g_id_value}" type="checkbox" {check_tag} />')

        tr_items.append(tr_item)
    # endregion

    if btn_actions:
        header_cols.append("操作")

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
    t_html = render_template_string(temp_html, cols=header_cols, tr_items=tr_items, show_selbox=show_selbox)
    return Markup(t_html)