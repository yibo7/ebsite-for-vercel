import re
from typing import Tuple

from bll.bll_base import BllBase
from eb_event import content_saving
from eb_utils.configs import SiteConstant
from eb_utils.mvc_pager import pager_html_admin
from entity.news_content_model import NewsContentModel


class NewsContent(BllBase[NewsContentModel]):
    def new_instance(self) -> NewsContentModel:
        model = NewsContentModel()
        model.column_1 = ''
        model.column_2 = ''
        model.column_3 = ''
        model.column_4 = ''
        model.column_5 = ''
        model.column_6 = ''
        model.column_7 = ''
        model.column_8 = ''
        model.column_9 = ''
        model.column_10 = ''
        model.column_11 = ''
        model.column_12 = ''
        model.column_13 = ''
        model.column_14 = ''
        model.column_15 = ''
        model.column_16 = ''
        model.column_17 = ''
        model.column_18 = ''
        model.column_19 = ''
        model.column_20 = ''
        model.column_21 = ''

        return model

    def save_content(self, model: NewsContentModel):
        content_saving.to_do(model)
        if model.title:
            self.save(model)

    def search_content(self, keyword: str, class_id: str, page_number: int) -> Tuple[list[NewsContentModel], str]:
        """
        模糊搜索
        :param keyword: 搜索的关键词, 不传入会搜索所有
        :param page_number: 页面码
        :param key_name: 要模糊搜索的字段
        :return:
        """
        page_size = SiteConstant.PAGE_SIZE_AD

        s_where = {}
        if keyword:
            regex_pattern = re.compile(f'.*{re.escape(keyword)}.*', re.IGNORECASE)  # IGNORE CASE 忽略大小写
            # s_where = {'title': {'$regex': regex_pattern}}
            # 构建查询条件
            s_where = {
                "$or": [
                    {"title": {"$regex": regex_pattern}},
                    {"info": {"$regex": regex_pattern}}
                ]
            }

        if class_id:
            s_where['class_id'] = class_id

        datas, i_count = self.find_pages(page_number, page_size, s_where)

        pager = pager_html_admin(i_count, page_number, page_size, {'k': keyword})
        return datas, pager
