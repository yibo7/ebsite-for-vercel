from dataclasses import replace

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


def get_table_data(data_source, cols, btn_actions=None):
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
