from entity.entity_base import ModelBase


class AdminUserModel(ModelBase):
    def __init__(self):
        super().__init__()
        self.user_name = ""
        self.user_pass = ""
        self.user_status = 0
        self.role_id = 0
        self.role_name = ""
        self.real_name = ""
        self.user_email = ""
        self.mobile_number = ""
