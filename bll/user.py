from werkzeug.security import generate_password_hash, check_password_hash

from bll.bll_base import BllBase
from db_utils import redis_utils
from entity.user_model import UserModel
from entity.user_token import UserToken


class User(BllBase[UserModel]):

    def new_instance(self) -> UserModel:
        return UserModel()

    def exist_name(self, name: str) -> bool:
        return True if self.find_one_by_where({'username': name}) else False

    def exist_mobile(self, mobile: str) -> bool:
        return True if self.find_one_by_where({'mobile_number': mobile}) else False

    def exist_email(self, email: str) -> bool:
        return True if self.find_one_by_where({'email_address': email}) else False

    def reg_user(self, model: UserModel):

        u_name = model.username
        if not u_name or self.exist_name(u_name):
            return False, '账号已存在或不能为空'

        email = model.email_address
        if email and self.exist_email(email):
            return False, 'EMAIL已存在或不能为空'

        mobile = model.mobile_number
        if mobile and self.exist_name(mobile):
            return False, '手机号已存在或不能为空'

        if len(model.password) < 6:
            return False, '密码长度至少是6位'

        model.password = generate_password_hash(model.password)

        _data_id = self.add(model)

        return True, _data_id

    @staticmethod
    def check_pass(pass_1, pass_2):
        """
        验证用户密码是否正确
        :param pass_2:
        :param pass_1:
        :return:
        """
        return check_password_hash(pass_1, pass_2)

    def get_by_name(self, name: str):
        return self.find_one_by_where({"username": name})

    def login(self, user_name, pass_word):
        user = self.get_by_name(user_name)
        is_sucessfull = False
        msg = "未知错误"
        if user:
            pass_1 = user.password
            is_sucessfull = self.check_pass(pass_1, pass_word)
            if is_sucessfull:
                utk = UserToken(user._id, user.username, user.ni_name, user.group_id, "")
                msg = redis_utils.set_ex_hours(utk, 24)
            else:
                msg = "用户名或密码错误"
        else:
            msg = "用户名不存在或密码错误"

        return [is_sucessfull, msg]
