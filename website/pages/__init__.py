import datetime

from flask import Blueprint, g, render_template, request, redirect, make_response

from bll.admin_login_log import AdminLoginLog
from bll.admin_user import AdminUser
from bll.user import User
from bll.user_group import UserGroup
from db_utils import redis_utils
from eb_utils.configs import WebPaths, SiteConstant
from eb_utils.image_code import ImageCode
from eb_utils.string_check import is_email, is_mobile
from entity.site_settings import get_settings
from entity.user_model import UserModel
from entity.user_token import UserToken

pages_blue = Blueprint('pages_blue', __name__)
from . import cms_page


@pages_blue.context_processor
def inject_site_name():
    """
    使用context_processor上下文件处理器，注入pages_blue下所有模板的公共变量
    """
    settings_model = get_settings()
    return {'SiteName': settings_model.site_name}


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
    resp = render_template("index.html")
    return resp


@pages_blue.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@pages_blue.route('/login', methods=['GET', 'POST'])
def login():
    err_msg = ""
    err_count = redis_utils.get_count('user_login_err_count')
    if request.method == 'POST':
        username = request.form.get("username", None)
        password = request.form.get("pass", None)
        image_code = request.form.get("code", None)
        if is_email(username) or is_mobile(username):
            is_safe = True
            if err_count > 0:
                is_safe, err_msg = ImageCode().check_code(image_code)
            if is_safe:
                is_safe, err_msg = User().login(username, password)
                if is_safe:
                    resp = make_response(redirect(WebPaths.USER_INDEX))
                    expires = datetime.datetime.now() + datetime.timedelta(hours=24)
                    resp.set_cookie(SiteConstant.COOKIE_TOKEN_KEY, err_msg, expires=expires)
                    return resp  # redirect(WebPaths.ADMIN_INDEX)
                else:
                    err_count = redis_utils.add_count_hour('user_login_err_count', 24)
        else:
            err_msg = "请输入有效的EMAIL或手机号"

    return render_template("login.html", is_safe_code=err_count > 0, err=err_msg)


@pages_blue.route('/reg', methods=['GET', 'POST'])
def reg():
    err_msg = None
    if request.method == 'POST':
        username = request.form.get("username", None)
        password = request.form.get("password", None)
        passwordr = request.form.get("repassword", None)
        image_code = request.form.get("code", None)

        if image_code:
            is_safe, err_msg = ImageCode().check_code(image_code)
            if not is_safe:
                err_msg = "验证码错误!"
        else:
            err_msg = "验证码无效!"

        is_username_email = False
        if username:
            if is_email(username):
                is_username_email = True
                # send email code
                pass
            elif is_mobile(username):
                # send mobile code
                pass
            else:
                err_msg = '请输入正确的手机号或EMAIL'
        else:
            err_msg = "用户名不能为空!"

        if not all([password, passwordr]) or password != passwordr:
            err_msg = "密码格式不对或两次密码不一至!"

        if len(password) < 6:
            err_msg = "密码长度要大于6!"

        if not err_msg:
            user = UserModel()
            user.username = username
            user.password = password
            if is_username_email:
                user.email_address = username
            else:
                user.mobile_number = username
            [is_ok, msg] = User().reg_user(user)
            if is_ok:
                utk = UserToken(msg, username, username, user.group_id, "普通会员")
                session_id = redis_utils.set_ex_hours(utk, 24)
                resp = make_response(redirect(WebPaths.USER_INDEX))
                expires = datetime.datetime.now() + datetime.timedelta(hours=24)
                resp.set_cookie(SiteConstant.COOKIE_TOKEN_KEY, session_id, expires=expires)
                return resp
            else:
                err_msg = msg
    return render_template("reg.html", err=err_msg)


@pages_blue.route('/reg_info.html', methods=['GET', 'POST'])
def reg_info():
    return render_template("reg_info.html")


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
