from werkzeug.security import generate_password_hash, check_password_hash

from bll.admin_role import AdminRole
from bll.bll_base import BllBase
from db_utils import redis_utils
from entity.admin_user_model import AdminUserModel
from entity.user_token import UserToken


class AdminUser(BllBase[AdminUserModel]):
    def new_instance(self) -> AdminUserModel:
        return AdminUserModel()

    # def __init__(self):
    #     super().__init__()

    def add_default(self):
        if not self.exist_table():
            roloe_id, roloe_name = AdminRole().add_default()
            model = self.new_instance()
            model.user_name = "admin"
            model.user_pass = generate_password_hash("222222")
            model.user_status = 1
            model.role_id = roloe_id
            model.role_name = roloe_name
            model.real_name = "创建人"
            return self.add(model)
        return None

    def get_by_name(self, name: str):
        return self.find_one_by_where({"user_name": name})

    @staticmethod
    def check_pass(pass_1, pass_2):
        """
        验证用户密码是否正确
        :param pass_2:
        :param pass_1:
        :return:
        """
        return check_password_hash(pass_1, pass_2)

    def set_login_err_count(self):
        redis_utils.generate_next_id()

    def login(self, user_name, pass_word):
        user = self.get_by_name(user_name)
        is_sucessfull = False
        msg = "未知错误"
        if user:
            pass_1 = user.user_pass
            is_sucessfull = self.check_pass(pass_1, pass_word)
            if is_sucessfull:
                utk = UserToken(user._id, user.user_name, user.real_name, user.role_id, user.role_name)
                msg = redis_utils.set_ex_hours(utk, 24)
            else:
                msg = "用户名或密码错误"
        else:
            msg = "用户名不存在或密码错误"

        return [is_sucessfull, msg]

    def exist_name(self, name: str) -> bool:
        return True if self.find_one_by_where({'user_name': name}) else False

    def exist_mobile(self, mobile: str) -> bool:
        return True if self.find_one_by_where({'mobile_number': mobile}) else False

    def exist_email(self, email: str) -> bool:
        return True if self.find_one_by_where({'user_email': email}) else False

    def reg_user(self, model: AdminUserModel):

        u_name = model.user_name
        if not u_name or self.exist_name(u_name):
            return False, '账号已存在或不能为空'

        email = model.user_email
        if not email or self.exist_email(email):
            return False, 'EMAIL已存在或不能为空'

        mobile = model.mobile_number
        if not mobile or self.exist_name(mobile):
            return False, '手机号已存在或不能为空'

        if len(model.user_pass) < 6:
            return False, '密码长度至少是6位'

        model.user_pass = generate_password_hash(model.user_pass)

        self.add(model)

        return True, '成功'

    def change_pass(self, old_pass, new_pass, re_new_pass, model: AdminUserModel):
        if not (old_pass or new_pass or re_new_pass):
            return False, '有必填项没有填写'
        elif len(old_pass) < 6 or len(new_pass) < 6:
            return False, '密码长度至少为6位'
        elif new_pass != re_new_pass:
            return False, '两次输入的密码不正确'

        if not self.check_pass(model.user_pass, old_pass):
            return False, '输入的旧密码不正确'

        model.user_pass = generate_password_hash(new_pass)

        self.update(model)

        return True, '修改成功'
