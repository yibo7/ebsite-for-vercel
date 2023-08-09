import pymongo

from bll.bll_base import BllBase
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
