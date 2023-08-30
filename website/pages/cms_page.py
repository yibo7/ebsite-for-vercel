from flask import render_template, render_template_string, abort

from bll.new_class import NewsClass
from bll.new_content import NewsContent
from bll.new_special import NewsSpecial
from bll.templates import Templates
from website.pages import pages_blue


@pages_blue.route('/c<int:id>p<int:p>.html', methods=['GET'])
def list(id: int, p: int):
    model = NewsClass().get_by_int_id(id)
    if model:
        bll = NewsContent()
        rewrite_rule = f'/c{id}p{{0}}.html'
        data_list, pager = bll.find_pager(p, model.page_size, rewrite_rule, {'class_id': str(model._id)})
        temp_model = Templates(1).find_one_by_id(model.class_temp_id)
        if temp_model.temp_model == 1:
            return render_template_string(temp_model.temp_code, model=model, data_list=data_list, pager=pager)
        else:
            return render_template(temp_model.file_path, model=model, data_list=data_list, pager=pager)
    abort(404)


@pages_blue.route('/a<int:id>.html', methods=['GET'])
def content(id: int):
    bll = NewsContent()
    model = bll.get_by_int_id(id)
    if model:
        class_model = NewsClass().find_one_by_id(model.class_id)
        if class_model:
            temp_model = Templates(2).find_one_by_id(class_model.content_temp_id)
            if temp_model.temp_model == 1:
                return render_template_string(temp_model.temp_code, model=model, class_model=class_model)
            else:
                return render_template(temp_model.file_path, model=model, class_model=class_model)
    abort(404)


@pages_blue.route('/s<int:id>p<int:p>.html', methods=['GET'])
def special(id: int, p:int):
    model = NewsSpecial().get_by_int_id(id)
    if model:
        temp_model = Templates(3).find_one_by_id(model.temp_id)
        query = {"id": {"$in": model.content_ids}}
        rewrite_rule = f'/s{id}p{{0}}.html'
        data_list, pager = NewsContent().find_pager(p, model.page_size, rewrite_rule, query)
        if temp_model.temp_model == 1:
            return render_template_string(temp_model.temp_code, model=model, data_list=data_list, pager=pager)
        else:
            return render_template(temp_model.file_path, model=model, data_list=data_list, pager=pager)
    abort(404)

