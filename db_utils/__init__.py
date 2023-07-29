import redis
from pymongo import MongoClient

# eb_db = SQLAlchemy()

# 创建Redis客户端实例
redis_db = redis.Redis(
    host='redis-10119.c252.ap-southeast-1-1.ec2.cloud.redislabs.com',
    port=10119,
    password='cejVttuqN1ogu1m4y31IVqsahjHDR6X7')

# 创建 MongoDB 客户端连接
mongo_client = MongoClient('mongodb+srv://mongo_u:mgdb2015@cqsmongo.d7plkb7.mongodb.net/?retryWrites=true&w=majority')
# 选择或创建数据库
mongo_db = mongo_client['xs_site']


def init_eb_db(app):
    """
    init mysql
    :param app:
    :return:
    """
    pass
    # app.config[
    #     'SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://media_db_user:123@mysql.sqlpub.com:3306/mydata"

    # 动态追踪数据库的修改. 性能不好. 且未来版本中会移除. 目前只是为了解决控制台的提示才写的
    # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # configs.IS_DEBUG
    # 查询时会显示原始SQL语句
    # app.config['SQLALCHEMY_ECHO'] = False  # configs.IS_DEBUG
    # global eb_db
    # eb_db.init_app(app)
    # eb_db.app = app  # 如果不加这个，在视图外使用会出错
