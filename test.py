import csv
import json
import os
from unittest import TestCase

from bson import ObjectId, json_util
from pymongo import MongoClient

from db_utils import OutputDefaultData
from eb_utils import http_utils


class testCode(TestCase):
    def testList(self):
        int_id = [1, 2, 3, 5, 6, 8, 9, 10]
        str_id = ['2', '3']

        int_id = [x for x in int_id if str(x) not in str_id]
        print('结果：')
        print(int_id)

    def testModelToDic(self):
        from entity.news_content_model import NewsContentModel
        model = NewsContentModel()
        dic_f = model.__dict__
        print(dic_f)

    def testOutputMongoDb(self):
        """
        项目发布前-导出安装默认需要的表及数据
        """
        OutputDefaultData()

    def testImportFromCsv(self):
        mongo_client = MongoClient('mongodb://localhost:27017')
        # 选择或创建数据库
        mongo_db = mongo_client['xs_site']

        csv_file = "http://127.0.0.1:8019/db_bak/AdminMenus.json"
        # 获取 CSV 文件的表名（去除文件扩展名）
        collection_name = os.path.splitext(os.path.basename(csv_file))[0]
        collection = mongo_db[collection_name]
        # 清空集合
        # mongo_db[collection_name].delete_many({})
        file = http_utils.getText(csv_file)
        json_data = json.loads(file, object_hook=json_util.object_hook)
        # with open(csv_file, "r") as file:
        #     json_data = json.load(file, object_hook=json_util.object_hook)
        #collection.insert_many(json_data)
