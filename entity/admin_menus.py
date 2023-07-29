import re

import pymongo
from bson import ObjectId

from db_utils import mongo_db
from eb_utils.configs import SiteConstant
from eb_utils.mvc_pager import pager_html_admin
from entity.entity_base import EntityBase


class AdminMenus(EntityBase):
    def __init__(self):
        super().__init__()
        self.menu_name: str = ""
        self.image_url: str = ""
        self.order_id: int = 0
        self.parent_id: str = ""
        self.page_url: str = ""
        self.is_menu: bool = True

    def get_by_pid(self, pid):
        s_where = {"parent_id": str(pid)}
        return self.find_list_by_where(s_where)

    def get_all_datas(self):
        datas = self.find_list_by_where("", "order_id", pymongo.ASCENDING)
        return datas

    def get_tree_text(self):
        get_tree = []
        datas = self.get_all_datas()

        for tree in datas:
            if not tree['parent_id']:
                tree['menu_name'] = f"╋{tree['menu_name']}"
                get_tree.append(tree)
                self.get_sub_item(tree['_id'], get_tree, "├", datas)

        return get_tree

    def get_sub_item(self, data_id, new_class, blank, old_class):
        for md_model in old_class:
            if md_model['parent_id'] == str(data_id):
                str_tag = f"{blank}─"
                md_model['menu_name'] = f"{str_tag}『{md_model['menu_name']}』"
                new_class.append(md_model)
                self.get_sub_item(md_model['_id'], new_class, str_tag, old_class)

    def reset_orderid(self):
        datas = self.get_by_pid("")
        self._reset_orderid(datas)

    def _reset_orderid(self, datas):
        if datas and len(datas) > 0:
            i_index = 0
            for model in datas:
                i_index += 1
                model["order_id"] = i_index
                self.update(model)
                datas_sub = self.get_by_pid(model.get("_id"))
                self._reset_orderid(datas_sub)

    def move_to(self, from_id, target_id, move_type: int):
        from_model = self.find_one_by_id(from_id)
        mongo_db[self.table_name].update_many(
            {
                "parent_id": from_model.get("parent_id"),
                "order_id": {"$gt": from_model.get("order_id")}
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
                    "parent_id": target_model.get("parent_id"),
                    "order_id": {"$gte": target_model.get("order_id")}
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
                    "$set": {"order_id": target_model.get('order_id'), "parent_id": target_model.get("parent_id")}
                }
            )


