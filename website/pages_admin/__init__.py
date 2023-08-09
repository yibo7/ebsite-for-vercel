from flask import Blueprint, g, render_template, request, redirect, make_response

from bll.user_group import UserGroup
from db_utils import redis_utils
from eb_utils import http_helper, update_dic_to_class
from eb_utils.configs import WebPaths, SiteConstant
from bll.admin_menus import AdminMenus
from entity.site_settings import get_settings
from entity.user_token import UserToken

admin_blue = Blueprint('admin', __name__, url_prefix=WebPaths.ADMIN_PATH)

from . import menus
from . import users
from . import adminer
from . import logs

from . import custom_form
from . import news_class
from . import news_content
from . import news_special
from . import widgets

# region 后台请求前的处理

@admin_blue.before_request
def before_req():
    """
    在后台页面请求前进行一些权限处理
    :return:
    """
    token_key = request.cookies.get(SiteConstant.COOKIE_AD_TOKEN_KEY)
    # g.u = None
    g.u = None
    if token_key:
        admin_token = redis_utils.get_obj(token_key)  # type:UserToken
        if admin_token:
            g.u = admin_token
            g.uid = admin_token.id
        # g.err = None

    if not g.u:
        return redirect("/login_ad")


# endregion

@admin_blue.route('index', methods=['GET'])
def admin_index():
    menu = AdminMenus().get_by_pid("")
    return render_template(WebPaths.get_admin_path("index.html"), menu_data=menu)


@admin_blue.route('wellcome', methods=['GET'])
def admin_wellcome():
    return render_template(WebPaths.get_admin_path("wellcome.html"))


@admin_blue.route('log_out', methods=['GET'])
def admin_log_out():
    token_key = request.cookies.get(SiteConstant.COOKIE_AD_TOKEN_KEY)
    if token_key:
        redis_utils.delete(token_key)
        resp = make_response(redirect(WebPaths.ADMIN_LOGIN))
        resp.delete_cookie(token_key)
        return resp
    redirect("/")


@admin_blue.route('settings', methods=['GET', 'POST'])
def admin_settings():
    settings_model = get_settings()

    if request.method == 'POST':
        prams_dict = http_helper.get_prams_dict()
        settings_model = update_dic_to_class(prams_dict, settings_model)
        # settings_model.is_open_safe_code = http_helper.get_prams('is_open_safe_code')
        settings_model.save()
    return render_template(WebPaths.get_admin_path("configs/settings.html"), model=settings_model,
                           group=UserGroup().find_all())
