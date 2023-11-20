import json
import os
import redis
from bson import json_util
from flask import request
from pymongo import MongoClient

from eb_utils import http_utils

# mongodb+srv://user:pass@cqsmongo.d7plkb7.mongodb.net/?retryWrites=true&w=majority
MONGODB_SERV = os.environ.get('MONGODB_SERV', 'mongodb://localhost:27017')
# redis://:userkey@redis-10119.c252.ap-southeast-1-1.ec2.cloud.redislabs.com:10119
REDIS_SERV = os.environ.get('REDIS_SERV', 'redis://127.0.0.1:6379')
MONGODB_NAME = os.environ.get('MONGODB_NAME', 'eb_site')  # xs_site
# eb_db = SQLAlchemy()
# 创建Redis客户端实例
redis_db = redis.from_url(REDIS_SERV)

# 创建 MongoDB 客户端连接
mongo_client = MongoClient(MONGODB_SERV)
# 选择或创建数据库
mongo_db = mongo_client[MONGODB_NAME]


def init_eb_db(app):
    """
    init mysql
    :param app:
    :return:
    """
    pass
    # app.config[
    #     'SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://test:123@mysql.sqlpub.com:3306/mydata"

    # 动态追踪数据库的修改. 性能不好. 且未来版本中会移除. 目前只是为了解决控制台的提示才写的
    # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # configs.IS_DEBUG
    # 查询时会显示原始SQL语句
    # app.config['SQLALCHEMY_ECHO'] = False  # configs.IS_DEBUG
    # global eb_db
    # eb_db.init_app(app)
    # eb_db.app = app  # 如果不加这个，在视图外使用会出错


# 发布项目默认备份还原的表
default_tables = ['AdminMenus', 'AdminRole', 'AdminUser', 'SiteModel', 'Templates', 'UserGroup', 'Widgets', 'NewsClass',
                  'NewsContent']


def OutputDefaultData():
    """
    备份表
    """
    for table_name in default_tables:
        # 获取数据库和集合
        collection = mongo_db[table_name]

        # 查询集合中的所有文档
        cursor = collection.find({})
        data = [document for document in cursor]
        data = json_util.dumps(data)

        with open(f'website/static/db_bak/{table_name}.json', 'w', encoding='utf-8') as file:
            file.write(data)


def ImportDefaultData():
    """
    还原表
    """
    for table_name in default_tables:
        collection_list = mongo_db.list_collection_names()
        if table_name not in collection_list:
            csv_file = f"{request.host_url}db_bak/{table_name}.json"
            txt = http_utils.getText(csv_file)
            # 获取 CSV 文件的表名(去除文件扩展名)
            collection_name = os.path.splitext(os.path.basename(csv_file))[0]
            collection = mongo_db[collection_name]

            json_data = json.loads(txt, object_hook=json_util.object_hook)
            # with open(csv_file, "r") as file:
            #     json_data = json.load(file, object_hook=json_util.object_hook)
            collection.insert_many(json_data)
