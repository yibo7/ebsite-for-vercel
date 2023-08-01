from entity.entity_base import ModelBase, annotation


class AdminUserModel(ModelBase):
    def __init__(self):
        super().__init__()
        self.user_name = ""
        self.user_pass = ""
        self.user_status = 0
        self.role_id = ""
        self.role_name = ""
        self.real_name = ""
        self.user_email = ""
        self.mobile_number = ""

    @annotation("账号名称")
    def a_user_name(self):
        return self.user_name

    @annotation("真实姓名")
    def b_real_name(self):
        return self.real_name

    @annotation("状态|adminer_status")
    def c_user_status(self):
        return self.user_status

    @annotation("角色名称")
    def c_role_name(self):
        return self.role_name

    @annotation("EMAIL")
    def d_user_status(self):
        return self.user_email

    @annotation("手机号")
    def e_mobile_number(self):
        return self.mobile_number

    @annotation("添加时间")
    def f_add_time(self):
        return self.add_time