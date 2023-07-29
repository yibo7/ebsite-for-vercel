import os

from flask import Flask

from db_utils import init_eb_db

basedir = os.path.abspath(os.path.dirname(__file__))


def create_app(run_mode):  # run_mode
    """
    创建app
    :param run_mode: str 运行方式 ("dev" | "pro")
    :return:
    """

    app = Flask(__name__, static_url_path='/')
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['TEMPLATES_AUTO_RELOAD'] = True  # 模板热更新
    init_eb_db(app)
    # db.app = app  # 如果不加这个，在视图外使用会出错
    # 将蓝图注册到app中
    from website.pages import pages_blue
    app.register_blueprint(pages_blue)
    from website.pages_admin import admin_blue
    app.register_blueprint(admin_blue)
    from website.pages.apis import api_blue
    app.register_blueprint(api_blue)

    # 注册自定义过滤器--让模板支持str()函数 在模板中调用 {% if item.get("_id")|str == model.parent_id %}
    app.jinja_env.filters['str'] = to_str

    # 启动时，手动加载BOT 后期更新bot会有dbsession混乱的问题
    # init_all_change(Event(EVENT_UPDATE_CHANGE,data="start"))
    return app


# 自定义过滤器：str
def to_str(value):
    return str(value)
