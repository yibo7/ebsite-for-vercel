from typing import Tuple

import pymongo
from bson import ObjectId

from bll.bll_base import BllBase
from bll.new_content import NewsContent
from eb_utils.configs import SiteConstant
from eb_utils.mvc_pager import pager_html_admin
from entity.news_content_model import NewsContentModel
from entity.news_special_model import NewsSpecialModel


class NewsSpecial(BllBase[NewsSpecialModel]):
    def new_instance(self) -> NewsSpecialModel:
        return NewsSpecialModel()

    def get_by_pid(self, pid) -> list[NewsSpecialModel]:
        s_where = {"parent_id": str(pid)}
        return self.find_list_by_where(s_where, "order_id", pymongo.ASCENDING)

    def get_all_datas(self) -> list[NewsSpecialModel]:
        datas = self.find_list_by_where("", "order_id", pymongo.ASCENDING)
        return datas

    def get_tree_text(self) -> list[NewsSpecialModel]:
        get_tree = []
        datas = self.get_all_datas()

        for tree in datas:
            if not tree.parent_id:
                tree.name = f"╋{tree.name}"
                get_tree.append(tree)
                self.get_sub_item_text(tree._id, get_tree, "├", datas)

        return get_tree

    def get_sub_item_text(self, data_id, new_class: list[NewsSpecialModel], blank: str,
                          old_class: list[NewsSpecialModel]):
        for md_model in old_class:
            if md_model.parent_id == str(data_id):
                str_tag = f"{blank}─"
                md_model.name = f"{str_tag}『{md_model.name}』"
                new_class.append(md_model)
                self.get_sub_item_text(md_model._id, new_class, str_tag, old_class)

    def get_tree(self):
        get_tree = []
        datas = self.get_all_datas()

        for tree in datas:
            if not tree.parent_id:
                tree.name = f"<img src='/images/tree/w1.gif' align=absmiddle><b><font color=green>{tree.name}</font></b>"
                get_tree.append(tree)
                self.get_sub_item(tree._id, get_tree, "", datas)

        return get_tree

    def get_sub_item(self, data_id, new_class, blank, old_class):

        sW3 = '<img src=\"/images/tree/w3.gif\" align=absmiddle>'
        sW1 = '<img src=\"/images/tree/w1.gif\" align=absmiddle>'

        for md_model in old_class:
            if md_model.parent_id == str(data_id):
                str_tag = f"{blank}{sW3}"
                md_model.name = f"{str_tag}{sW1}{md_model.name}"
                new_class.append(md_model)
                self.get_sub_item(md_model._id, new_class, str_tag, old_class)

    def save_content_to_special(self, ids: [str], special_ids: [str]):
        content_ids = [ObjectId(data_id) for data_id in ids]
        query = {"_id": {"$in": content_ids}}
        content_data = NewsContent().find_list_by_where(query)
        int_ids = [data.id for data in content_data]
        for sp_id in special_ids:
            model = self.find_one_by_id(sp_id)
            model.content_ids = list(set(model.content_ids + int_ids))
            self.save(model)

    def get_by_speical_id(self, s_id: str, page_number: int) -> Tuple[list[NewsContentModel], str]:
        """
        模糊搜索
        :param s_id: 专题ID
        :param page_number: 页面码
        :return:
        """
        page_size = SiteConstant.PAGE_SIZE_AD
        model = self.find_one_by_id(s_id)
        s_where = {"id": {"$in": model.content_ids}}
        datas, i_count = NewsContent().find_pages(page_number, page_size, s_where)

        pager = pager_html_admin(i_count, page_number, page_size, {'sid': s_id})
        return datas, pager

    def del_content(self, sid: str, ids: str):
        if ids:
            model = self.find_one_by_id(sid)
            str_id = ids.split(',')
            if 'on' in str_id:
                str_id.remove('on')

            content_ids = [ObjectId(data_id) for data_id in str_id]
            query = {"_id": {"$in": content_ids}}
            content_data = NewsContent().find_list_by_where(query)
            content_int_ids = [data.id for data in content_data]

            int_id = model.content_ids
            int_id = [x for x in int_id if x not in content_int_ids]
            model.content_ids = int_id
            self.save(model)

    def clear_content(self, sid: str):
        model = self.find_one_by_id(sid)
        model.content_ids = []
        self.save(model)