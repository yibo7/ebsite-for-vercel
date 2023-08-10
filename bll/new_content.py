import re
from typing import Tuple

from bll.bll_base import BllBase
from eb_utils.configs import SiteConstant
from eb_utils.mvc_pager import pager_html_admin
from entity.news_content_model import NewsContentModel


class NewsContent(BllBase[NewsContentModel]):
    def new_instance(self) -> NewsContentModel:
        return NewsContentModel()

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


