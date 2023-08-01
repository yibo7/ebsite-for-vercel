from werkzeug.security import generate_password_hash, check_password_hash

from bll.bll_base import BllBase
from db_utils import redis_utils
from entity.admin_role_model import AdminRoleModel
from entity.user_token import UserToken


class AdminRole(BllBase[AdminRoleModel]):
    def new_instance(self) -> AdminRoleModel:
        return AdminRoleModel()

    # def __init__(self):
    #     super().__init__()

    def add_default(self):
        role_id = None
        if not self.exist_table():
            model = self.new_instance()
            model.user_name = "超级管理员"
            model.info = "拥有所有权限"
            role_id = self.add(model)
        else:
            role_id = self.find_one_first()._id
        return role_id,'超级管理员'

    def exist_name(self, name: str) -> bool:
        return True if self.find_one_by_where({'name': name}) else False

    def add_pos(self,role_id:str, pos_ids: str):
        a_pos_id = pos_ids.split(',')
        if 'on' in a_pos_id:
            a_pos_id.remove('on')
        model = self.find_one_by_id(role_id)
        model.pos_id = a_pos_id
        self.update(model)