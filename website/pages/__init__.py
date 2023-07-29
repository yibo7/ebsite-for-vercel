import datetime

from flask import Blueprint, g, render_template, request, redirect, make_response

from db_utils import redis_utils
from eb_utils.configs import WebPaths, SiteConstant
from eb_utils.image_code import ImageCode
from entity.admin_user import AdminUser
from entity.user_group import UserGroup

pages_blue = Blueprint('pages_blue', __name__)


@pages_blue.before_request
def before_req():
    """
    在页面请求前进行一些权限处理
    :return:
    """
    g.userid = None
    print("请求了页面...")


@pages_blue.route('/', methods=['GET'])
def welcome():
    resp = make_response(render_template("site_index.html"))
    return resp


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

    return render_template("site_login.html", err=err_msg)


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

    return render_template("site_reg.html", err=err_msg)


@pages_blue.route('/login_ad', methods=['GET', 'POST'])
def ad_login():
    err_msg = ""
    AdminUser().add_default()
    UserGroup().add_default()
    if request.method == 'POST':
        # session.pop(SessionIds.User, None)
        username = request.form.get("username", None)
        password = request.form.get("pass", None)
        image_code = request.form.get("code", None)
        safe_key = request.form.get("key", None)
        if image_code and redis_utils.exists_key(safe_key):
            safe_code = redis_utils.get_str(safe_key).lower()
            if image_code.lower() == safe_code:
                [is_ok, msg] = AdminUser().login(username, password)
                if is_ok:
                    resp = make_response(redirect(WebPaths.ADMIN_INDEX))
                    expires = datetime.datetime.now() + datetime.timedelta(hours=24)
                    resp.set_cookie(SiteConstant.COOKIE_AD_TOKEN_KEY, msg, expires=expires)
                    return resp  # redirect(WebPaths.ADMIN_INDEX)
                else:
                    err_msg = msg
            else:
                err_msg = "验证码错误"
        else:
            err_msg = "验证码无效或过期"
    cache_key = redis_utils.generate_key()
    return render_template("admin/login.html", err=err_msg, safe_code_key=cache_key)


@pages_blue.route('/imgcode')
def img_code():
    cache_key = request.args.get("key", None)
    if cache_key:
        return ImageCode().getImgCode(cache_key)
    else:
        return "bad key"
