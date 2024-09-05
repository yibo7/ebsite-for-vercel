import os

from flask import Flask

from db_utils import init_eb_db
from eb_cache import init_eb_cache
from eb_triggers import init_triggers
from temp_expand import reg_temp_expand


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

    reg_temp_expand(app)

    init_eb_cache(app)

    # db.app = app  # 如果不加这个，在视图外使用会出错
    # 将蓝图注册到app中
    # from website.pages import register_routes
    # register_routes()
    from website.pages import pages_blue
    app.register_blueprint(pages_blue)
    from website.pages_admin import admin_blue
    app.register_blueprint(admin_blue)
    from website.pages.apis import api_blue
    app.register_blueprint(api_blue)
    from website.pages_ucc import user_blue
    app.register_blueprint(user_blue)

    init_triggers()

    return app
