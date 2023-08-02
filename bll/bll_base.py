import re
import time
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar, Tuple

import pymongo
from bson import ObjectId

from db_utils import mongo_db
from db_utils.redis_utils import generate_next_id
from eb_utils.configs import SiteConstant
from eb_utils.mvc_pager import pager_html_admin

T = TypeVar('T')  # 定义一个类型变量 T


class BllBase(Generic[T], ABC):
    def __init__(self):
        self.table_name = type(self).__name__

    def get_int_id(self):
        return generate_next_id(self.table_name)

    def exist_table(self):
        return self.table_name in mongo_db.list_collection_names()

    # def get_dic(self):
    #     data = self.__dict__
    #     data.pop("table_name")
    #     return data

    def add(self, model: T):
        model._id = ObjectId()
        if hasattr(model, 'id'):
            model.id = self.get_int_id()
        data_dic = model.__dict__
        result = mongo_db[self.table_name].insert_one(data_dic)
        return result.inserted_id

    def delete_by_id(self, _id):
        # 删除单个文档
        if isinstance(_id, str):
            _id = ObjectId(_id)
        s_where = {"_id": _id}
        return mongo_db[self.table_name].delete_one(s_where)

    def delete_by_ids(self, ids: [str]):
        """
        同时删除多个指定id的记录
        :param ids: id 列表，如 ["_id1", "_id2", "_id3"]
        :return:
        """
        # 构建筛选条件
        new_ids = []
        for data_id in ids:
            new_ids.append(ObjectId(data_id))
        s_where = {"_id": {"$in": new_ids}}
        # 执行删除操作
        return self.delete_by_where(s_where)

    # @admin_action_log("删除用户")
    def delete_from_page(self, s_id):
        if s_id:
            a_id = s_id.split(',')
            if 'on' in a_id:
                a_id.remove('on')
            self.delete_by_ids(a_id)

    def delete_by_where(self, d_where):
        """
        删除指定条件下的记录
        :param d_where: 条件，如 {"_id": {"$in": ids}}
        :return:
        """
        # 执行删除操作
        try:
            # print(d_where)
            result = mongo_db[self.table_name].delete_many(d_where)
            # print(f"Deleted {result.deleted_count} documents.")
            return result
        except Exception as e:
            print(f"MongoDb Delete err: {str(e)}")

    def update(self, model: T) -> bool:
        """
        更新一条数据
        :param model: 是一个document对象
        :param _id: 要更新的记录id,如果不指定将会在model中查找，如果包含_id将直接更新这个_id对应的记录，如果无_id将采用，如果都不指定id,不作更新
        :return: 是否更新成功
        """
        where = {"_id": model._id}
        # if "_id" in model:
        #     where = {"_id": model._id}
        # elif _id:
        #     where = {"_id": ObjectId(_id)}
        new_values = {"$set": model.__dict__}
        if where:
            mongo_db[self.table_name].update_one(where, new_values)
            return True
        return False

    def save(self, model: T):
        inserted_id = None
        if model:
            if model._id:
                self.update(model)
                inserted_id = model._id
            else:
                inserted_id = self.add(model)
        return inserted_id

    def find_one_first(self) -> T:
        # 查询单个文档
        document = mongo_db[self.table_name].find_one()
        return self.build_model(document)

    def find_one_by_id(self, _id: str) -> T:
        # 查询单个文档
        # document = mongo_db[self.table_name].find_one({"_id": ObjectId(_id)})
        # return self.build_model(document)
        return self.find_one_by_where({"_id": ObjectId(_id)})

    def find_one_by_where(self, where: {}) -> T:
        # 查询单个文档
        document = mongo_db[self.table_name].find_one(where)
        if document:
            return self.build_model(document)
        return None

    def find_list_by_where(self, where: {}, sort_key="_id", sort_direction=pymongo.DESCENDING) -> list[T]:
        """
        查询列表
        :param where: 查询条件 如：{"name":"ctt"}
        :param sort_key: 要用哪个字段排序，默认使用_id
        :param sort_direction: 排序方式，默认使用 pymongo.DESCENDING 降序排序
        :return: 结果列表，可以通过 for data in datas 遍历
        """
        if not where:
            where = {}
        datas = mongo_db[self.table_name].find(where).sort(sort_key, sort_direction)
        lst = []
        for document in datas:
            lst.append(self.build_model(document))
        return lst  # list(datas)

    def find_all(self) -> list[T]:
        """
        查询列表-所有
        :return: 结果列表，可以通过 for data in datas 遍历
        """
        return self.find_list_by_where({})

    def count(self, s_where: {}):
        c = mongo_db[self.table_name].count_documents(s_where)
        return c

    def find_pages(self, page_number: int, page_size: int, where={}, sort_key="_id",
                   sort_direction=pymongo.DESCENDING) -> Tuple[list[T], str]:
        """
        分页查询列表
        :param page_size: 每页的记录数
        :param page_number: 页码，从1开始
        :param where: 查询条件 如：{"name":"ctt"} 默认不填写将查询全部
        :param sort_key: 要用哪个字段排序，默认使用_id
        :param sort_direction: 排序方式，默认使用 pymongo.DESCENDING 降序排序
        :return: 结果列表，可以通过 for data in datas 遍历
        """

        # 计算跳过的文档数量
        skip_count = (page_number - 1) * page_size

        # 执行分页查询并排序
        datas = mongo_db[self.table_name].find(where).skip(skip_count).limit(page_size).sort(sort_key, sort_direction)
        if datas:
            c = self.count(where)
            lst = []
            for document in datas:
                lst.append(self.build_model(document))
            return c, lst
        return None

    def search(self, keyword: str, page_number: int, key_name: str) -> Tuple[list[T], str]:
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
            s_where = {key_name: {'$regex': regex_pattern}}

        i_count, datas = self.find_pages(page_number, page_size, s_where)

        pager = pager_html_admin(i_count, page_number, page_size, {'k': keyword})
        return datas, pager

    @abstractmethod
    def new_instance(self) -> T:
        pass

    def build_model(self, dic_data: dict):
        model = self.new_instance()
        model.dict_to_model(dic_data)
        return model

