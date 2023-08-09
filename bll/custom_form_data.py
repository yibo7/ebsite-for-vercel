import pymongo
from bson import ObjectId

from bll.custom_form import CustomForm
from db_utils import mongo_db


class CustomFormData:
    def __init__(self, f_id: str):
        self.f_id = f_id
        model = CustomForm().find_one_by_id(f_id)
        self.table_name = f'CustomForm{model.id}'

    def add(self, data: dict):
        result = mongo_db[self.table_name].insert_one(data)
        return result.inserted_id

    def delete_by_id(self, _id):
        # 删除单个文档
        if isinstance(_id, str):
            _id = ObjectId(_id)
        s_where = {"_id": _id}
        return mongo_db[self.table_name].delete_one(s_where)

    def count(self, s_where: {}):
        c = mongo_db[self.table_name].count_documents(s_where)
        return c

    def find_pages(self, page_number: int, page_size: int, where=None, sort_key="_id",
                   sort_direction=pymongo.DESCENDING):
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
        if where is None:
            where = {}
        skip_count = (page_number - 1) * page_size

        # 执行分页查询并排序
        datas = mongo_db[self.table_name].find(where).skip(skip_count).limit(page_size).sort(sort_key, sort_direction)
        if datas:
            c = self.count(where)
            lst = []
            for document in datas:
                lst.append(document)
            return c, lst
        return None
