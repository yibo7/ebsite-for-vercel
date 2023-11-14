import inspect

import pymongo
from bson import ObjectId

from bll.bll_base import BllBase
from db_utils import mongo_db
from eb_event import class_saving
from entity.news_class_model import NewsClassModel


class NewsClass(BllBase[NewsClassModel]):
    def new_instance(self) -> NewsClassModel:
        return NewsClassModel()

    def save_class(self, model: NewsClassModel):
        class_saving.to_do(model)
        if model.class_name:
            self.save(model)

    def get_by_pid(self, pid) -> list[NewsClassModel]:
        s_where = {"parent_id": str(pid)}
        return self.find_list_by_where(s_where, "order_id", pymongo.ASCENDING)

    def get_all_datas(self) -> list[NewsClassModel]:
        datas = self.find_list_by_where("", "order_id", pymongo.ASCENDING)
        return datas

    def get_tree_text(self) -> list[NewsClassModel]:
        get_tree = []
        datas = self.get_all_datas()

        for tree in datas:
            if not tree.parent_id:
                tree.class_name = f"╋{tree.class_name}"
                get_tree.append(tree)
                self.get_sub_item_text(tree._id, get_tree, "├", datas)

        return get_tree

    def get_sub_item_text(self, data_id, new_class: list[NewsClassModel], blank: str, old_class: list[NewsClassModel]):
        for md_model in old_class:
            if md_model.parent_id == str(data_id):
                str_tag = f"{blank}─"
                md_model.class_name = f"{str_tag}『{md_model.class_name}』"
                new_class.append(md_model)
                self.get_sub_item_text(md_model._id, new_class, str_tag, old_class)

    def get_tree(self):
        get_tree = []
        datas = self.get_all_datas()

        for tree in datas:
            if not tree.parent_id:
                tree.class_name = f"<img src='/images/tree/w1.gif' align=absmiddle><b><font color=green>{tree.class_name}</font></b>"
                get_tree.append(tree)
                self.get_sub_item(tree._id, get_tree, "", datas)

        return get_tree

    def get_sub_item(self, data_id, new_class, blank, old_class):

        sW3 = '<img src=\"/images/tree/w3.gif\" align=absmiddle>'
        sW1 = '<img src=\"/images/tree/w1.gif\" align=absmiddle>'

        for md_model in old_class:
            if md_model.parent_id == str(data_id):
                str_tag = f"{blank}{sW3}"
                md_model.class_name = f"{str_tag}{sW1}{md_model.class_name}"
                new_class.append(md_model)
                self.get_sub_item(md_model._id, new_class, str_tag, old_class)

    def reset_orderid(self):
        datas = self.get_by_pid("")
        self._reset_orderid(datas)

    def _reset_orderid(self, datas):
        if datas and len(datas) > 0:
            i_index = 0
            for model in datas:
                i_index += 1
                model.order_id = i_index
                self.update(model)
                datas_sub = self.get_by_pid(model._id)
                self._reset_orderid(datas_sub)

    def move_to(self, from_id, target_id, move_type: int):
        from_model = self.find_one_by_id(from_id)
        mongo_db[self.table_name].update_many(
            {
                "parent_id": from_model.parent_id,
                "order_id": {"$gt": from_model.order_id}
            },
            {
                "$inc": {"order_id": -1}
            }
        )
        if move_type == 1:  # 作为目标分类的子分类
            mongo_db[self.table_name].update_many(
                {
                    "parent_id": target_id
                },
                {
                    "$inc": {"order_id": 1}
                }
            )
            mongo_db[self.table_name].update_many(
                {
                    "_id": ObjectId(from_id)
                },
                {
                    "$set": {"order_id": 1, "parent_id": target_id}
                }
            )
        else:  # 移动到某个分类前面
            target_model = self.find_one_by_id(target_id)
            mongo_db[self.table_name].update_many(
                {
                    "parent_id": target_model.parent_id,
                    "order_id": {"$gte": target_model.order_id}
                },
                {
                    "$inc": {"order_id": 1}
                }
            )
            mongo_db[self.table_name].update_many(
                {
                    "_id": ObjectId(from_id)
                },
                {
                    "$set": {"order_id": target_model.order_id, "parent_id": target_model.parent_id}
                }
            )
