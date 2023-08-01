from werkzeug.security import generate_password_hash

from bll.bll_base import BllBase
from entity.user_model import UserModel


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
        if not email or self.exist_email(email):
            return False, 'EMAIL已存在或不能为空'

        mobile = model.mobile_number
        if not mobile or self.exist_name(mobile):
            return False, '手机号已存在或不能为空'

        if len(model.password) < 6:
            return False, '密码长度至少是6位'

        model.password = generate_password_hash(model.password)

        self.add(model)

        return True, '成功'
