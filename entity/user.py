import time

from entity.entity_base import EntityBase


class User(EntityBase):
    def __int__(self):
        self.username = ""
        self.password = ""
        self.mobile_number = ""
        self.email_address = ""
        self.is_locked = False
        self.last_login_date = time.time()
        self.last_login_ip = ""
        self.credits = 0
        self.ni_name = ""
        self.reg_remark = ""
        self.group_id = ""
        self.login_count = 0
        self.id = self.get_int_id()
