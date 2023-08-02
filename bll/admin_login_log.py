from bll.bll_base import BllBase
from eb_utils import http_helper
from entity.admin_login_log_model import AdminLoginLogModel


class AdminLoginLog(BllBase[AdminLoginLogModel]):
    def new_instance(self) -> AdminLoginLogModel:
        return AdminLoginLogModel()

    def add_log(self,user_name: str, ni_name: str,  title: str, content: str,user_id=''):
        model = self.new_instance()
        model.title = title
        model.description = content
        model.user_id = user_id
        model.user_name = user_name
        model.ni_name = ni_name
        model.ip_addr = http_helper.get_ip()

        self.add(model)