import ast
import json

import pymongo
from bson import ObjectId
from flask import render_template_string
from markupsafe import Markup

from bll.bll_base import BllBase
from bll.new_class import NewsClass
from bll.new_content import NewsContent
from bll.new_special import NewsSpecial
from bll.user import User
from entity.list_item import ListItem
from entity.widgets_model import WidgetsModel


class Widgets(BllBase[WidgetsModel]):
    def new_instance(self) -> WidgetsModel:
        return WidgetsModel()

    def get_desc_asc(self):
        lst = [ListItem(value='DESC', name='DESC'), ListItem(value='ASC', name='ASC')]
        return lst

    def get_content(self, _id: str):
        model = self.find_one_by_id(_id)
        if model:
            if model.temp_type == 5:  # text
                return model.temp_code
            elif model.temp_type == 6:  # html
                return Markup(model.temp_code)
            else:
                s_where = {}
                if model.where_query:
                    s_where = ast.literal_eval(model.where_query)
                    # literal_eval 无法解析带有类型的字典，如 ObjectId "{'_id': ObjectId('64d2e7c93798563b080040c4')}"
                    # 如要查询指定id的记录，可查询 自增加 id
                    # s_where = eval(model.where_query, {'ObjectId': ObjectId}) # eval 比较危险，但功能强大

                order_by = model.order_by
                desc_asc = pymongo.DESCENDING if model.order_by_desc == 'DESC' else pymongo.ASCENDING
                int_limit = model.limit

                bll = self.get_type_by_id(model.temp_type).get('bll')

                data = bll.find_list_by_where(s_where, order_by, desc_asc, int_limit)

                return Markup(render_template_string(model.temp_code, data=data))

        return f'can`t find widget:{_id}'

    def get_types(self):
        return [
            {'id': 1, 'name': '分类查询部件', 'info': '此部件用来获取分类相关的数据', 'bll': NewsClass()},
            {'id': 2, 'name': '内容查询部件', 'info': '获取内容相关的数据', 'bll': NewsContent()},
            {'id': 3, 'name': '专题查询部件', 'info': '查询并获取专题相关的数据', 'bll': NewsSpecial()},
            {'id': 4, 'name': '用户查询部件', 'info': '查询并获取用户相关的数据', 'bll': User()},
            {'id': 5, 'name': '文本框内容', 'info': '简单的文本框输入，并将内容呈现在模板'},
            {'id': 6, 'name': 'HTML编辑框', 'info': '可以在线编辑html内容'},
        ]

    def get_type_by_id(self, data_id: int):
        wg_types = self.get_types()
        record = next((item for item in wg_types if item['id'] == data_id), None)
        return record
