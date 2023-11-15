from flask import Blueprint, g, render_template, request, redirect, make_response

from bll.user_group import UserGroup
from db_utils import redis_utils
from eb_utils import http_helper, update_dic_to_class
from eb_utils.configs import WebPaths, SiteConstant
from bll.admin_menus import AdminMenus
from entity.site_settings import get_settings
from entity.user_token import UserToken

user_blue = Blueprint('user', __name__, url_prefix=WebPaths.USER_PATH)

@user_blue.context_processor
def inject_site_name():
    """
    使用context_processor上下文件处理器，注入pages_blue下所有模板的公共变量
    """
    settings_model = get_settings()
    return {'SiteName': settings_model.site_name}
# region 后台请求前的处理

@user_blue.before_request
def before_req():
    """
    在后台页面请求前进行一些权限处理
    :return:
    """
    token_key = request.cookies.get(SiteConstant.COOKIE_TOKEN_KEY)
    # g.u = None
    g.u = None
    if token_key:
        user_token = redis_utils.get_obj(token_key)  # type:UserToken
        if user_token:
            g.u = user_token
            g.uid = user_token.id
        # g.err = None

    if not g.u:
        return redirect("/login")


# endregion

@user_blue.route('index', methods=['GET'])
def user_index():
    return render_template(WebPaths.get_user_path("index.html"), user=g.u)


@user_blue.route('log_out', methods=['GET'])
def user_log_out():
    token_key = request.cookies.get(SiteConstant.COOKIE_TOKEN_KEY)
    if token_key:
        redis_utils.delete(token_key)
        resp = make_response(redirect(WebPaths.LOGIN_URL))
        resp.delete_cookie(token_key)
        return resp
    redirect("/")
