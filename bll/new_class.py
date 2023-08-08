import pymongo

from bll.bll_base import BllBase
from entity.news_class_model import NewsClassModel


class NewsClass(BllBase[NewsClassModel]):
    def new_instance(self) -> NewsClassModel:
        return NewsClassModel()

    def get_by_pid(self, pid) -> list[NewsClassModel]:
        s_where = {"parent_id": str(pid)}
        return self.find_list_by_where(s_where, "order_id", pymongo.ASCENDING)

    def get_all_datas(self)-> list[NewsClassModel]:
        datas = self.find_list_by_where("", "order_id", pymongo.ASCENDING)
        return datas

    def get_tree_text(self) -> list[NewsClassModel]:
        get_tree = []
        datas = self.get_all_datas()

        for tree in datas:
            if not tree.parent_id:
                tree.class_nane = f"╋{tree.class_nane}"
                get_tree.append(tree)
                self.get_sub_item_text(tree._id, get_tree, "├", datas)

        return get_tree

    def get_sub_item_text(self, data_id, new_class: list[NewsClassModel], blank: str, old_class: list[NewsClassModel]):
        for md_model in old_class:
            if md_model.parent_id == str(data_id):
                str_tag = f"{blank}─"
                md_model.class_nane = f"{str_tag}『{md_model.class_nane}』"
                new_class.append(md_model)
                self.get_sub_item_text(md_model._id, new_class, str_tag, old_class)