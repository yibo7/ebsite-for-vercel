import datetime

from flask import Blueprint, g, render_template, request, redirect, make_response, render_template_string, abort

from bll.admin_login_log import AdminLoginLog
from bll.admin_user import AdminUser
from bll.user_group import UserGroup
from db_utils import redis_utils
from eb_utils.configs import WebPaths, SiteConstant
from eb_utils.image_code import ImageCode

pages_blue = Blueprint('pages_blue', __name__)
from . import cms_page

# region load custom route
# def register_routes():
#     route = f"/list1p1.html"
#     pages_blue.add_url_rule(route, view_func=class_route_fun)
#
#
# def class_route_fun():
#     resp = render_template("list.html")
#     return resp
# endregion


@pages_blue.before_request
def before_req():
    """
    在页面请求前进行一些权限处理
    :return:
    """
    g.uid = None
    g.u = None
    print("请求了页面...")


@pages_blue.route('/', methods=['GET'])
def welcome():
    #
    # data = {'name': 'cqs'}
    # print('发送数据: ')
    # print(data)
    # content_ev.to_do(data)
    # print('修改后数据: ')
    # print(data)
    resp = render_template("index.html")
    return resp


@pages_blue.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@pages_blue.route('/login', methods=['GET', 'POST'])
def login():
    err_msg = ""
    if request.method == 'POST':
        # session.pop(SessionIds.User, None)
        username = request.form.get("username", None)
        password = request.form.get("pass", None)
        image_code = request.form.get("code", None)

        # if image_code and SessionIds.ImageCode in session:
        #     if image_code.lower() == session[SessionIds.ImageCode].lower():
        #         [is_ok, msg] = Users.login(username, password)
        #         if is_ok:
        #             session[SessionIds.User] = msg
        #             return redirect(WebPaths.USER_INDEX)
        #         else:
        #             err_msg = msg
        #     else:
        #         err_msg = "验证码错误"
        # else:
        #     err_msg = "验证码无效"

    return render_template("login.html", err=err_msg)


@pages_blue.route('/reg', methods=['GET', 'POST'])
def reg():
    err_msg = None
    # if request.method == 'POST':
    #     session.pop(SessionIds.User, None)
    #     username = request.form.get("username", None)
    #     password = request.form.get("password", None)
    #     passwordr = request.form.get("repassword", None)
    #     image_code = request.form.get("code", None)
    #
    #     if username:
    #         username = username.strip()
    #         if len(username) < 5:
    #             err_msg = "用户名格式不正确!"
    #         elif not XsStringVal.is_email(username):
    #             err_msg = "用户名请输入正确的EMAIL!"
    #     else:
    #         err_msg = "用户名不能为空!"
    #
    #     if image_code and SessionIds.ImageCode in session:
    #         if len(image_code) < 4 or image_code.lower() != session[SessionIds.ImageCode].lower():
    #             err_msg = "验证码错误!"
    #     else:
    #         err_msg = "验证码无效!"
    #
    #     if not all([password, passwordr]) or password != passwordr:
    #         err_msg = "密码格式不对或两次密码不一至!"
    #
    #     if len(password) < 6:
    #         err_msg = "密码长度要大于6!"
    #
    #     if not err_msg:
    #         user = Users(user_name=username, email=username, mobile="", real_name=username.split("@")[0])
    #         user.hash_pass = password
    #         user.gid = str(uuid.uuid4())
    #         [is_ok, msg] = user.save()
    #         if is_ok:
    #             session[SessionIds.User] = user.gid
    #             return redirect(WebPaths.USER_INDEX)
    #         else:
    #             err_msg = msg
    cache_key = redis_utils.get_safe_coe_key()
    return render_template("reg.html", err=err_msg, safe_code_key=cache_key)


@pages_blue.route('/login_ad', methods=['GET', 'POST'])
def ad_login():
    err_msg = ""
    AdminUser().add_default()
    UserGroup().add_default()
    err_count = redis_utils.get_count('adminer_login_err_count')

    if request.method == 'POST':
        # session.pop(SessionIds.User, None)
        username = request.form.get("username", None)
        password = request.form.get("pass", None)
        image_code = request.form.get("code", None)
        is_safe = True
        if err_count > 0:
            is_safe, err_msg = ImageCode().check_code(image_code)
        if is_safe:
            is_safe, err_msg = AdminUser().login(username, password)
            if is_safe:
                resp = make_response(redirect(WebPaths.ADMIN_INDEX))
                expires = datetime.datetime.now() + datetime.timedelta(hours=24)
                resp.set_cookie(SiteConstant.COOKIE_AD_TOKEN_KEY, err_msg, expires=expires)
                return resp  # redirect(WebPaths.ADMIN_INDEX)
            else:
                err_count = redis_utils.add_count_hour('adminer_login_err_count', 24)

        AdminLoginLog().add_log(username, username, '后台登录失败', err_msg)

    # settings_model = get_settings()
    return render_template("admin/login.html", is_safe_code=err_count > 0, err=err_msg)


@pages_blue.route('/imgcode')
def img_code():
    return ImageCode().getImgCode()
