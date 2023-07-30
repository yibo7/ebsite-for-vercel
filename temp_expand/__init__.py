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
