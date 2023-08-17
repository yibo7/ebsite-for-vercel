import pymongo
from bson import ObjectId

from db_utils import mongo_db
from entity.custom_form_model import CustomFormModel


class CustomFormData:
    def __init__(self):
        self.table_name = f'CustomFormData'

    def add(self, form_model: CustomFormModel, data: dict):
        name_values = [field["name"] for field in form_model.fields]
        for k, v in data.items():
            if len(v) > form_model.max_len:
                return False, f'{k} 提交内容超出长度限制'
            if k not in name_values:
                return False, f'{k} 非当前表单模型'

        data['form_id'] = str(form_model._id)
        result = mongo_db[self.table_name].insert_one(data)
        # return result.inserted_id
        return True, str(result.inserted_id)


    def delete_from_page(self, s_id):
        if s_id:
            a_id = s_id.split(',')
            if 'on' in a_id:
                a_id.remove('on')
            self.delete_by_ids(a_id)

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

    def delete_by_id(self, _id):
        # 删除单个文档
        if isinstance(_id, str):
            _id = ObjectId(_id)
        s_where = {"_id": _id}
        return mongo_db[self.table_name].delete_one(s_where)

    def count(self, s_where: {}):
        c = mongo_db[self.table_name].count_documents(s_where)
        return c



    def find_pages(self, page_number: int, page_size: int, form_model: CustomFormModel, sort_key="_id",
                   sort_direction=pymongo.DESCENDING):
        """
        分页查询列表
        :param page_size: 每页的记录数
        :param page_number: 页码，从1开始
        :param form_model: 表单
        :param sort_key: 要用哪个字段排序，默认使用_id
        :param sort_direction: 排序方式，默认使用 pymongo.DESCENDING 降序排序
        :return: 结果列表，可以通过 for data in datas 遍历
        """
        where = {'form_id': str(form_model._id)}
        skip_count = (page_number - 1) * page_size
        name_values = [field["name"] for field in form_model.fields]
        # 执行分页查询并排序
        datas = mongo_db[self.table_name].find(where).skip(skip_count).limit(page_size).sort(sort_key, sort_direction)
        if datas:
            c = self.count(where)
            lst = []
            for document in datas:
                new_data = {"_id": document.get('_id')}
                for key, value in document.items():
                    if key in name_values:
                        new_data[key] = value

                lst.append(new_data)
            return c, lst
        return None, None
