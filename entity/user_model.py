import time

from entity.entity_base import ModelBase, annotation


class UserModel(ModelBase):
    def __init__(self):
        super().__init__()
        self.ni_name = ""
        self.username = ""
        self.password = ""
        self.mobile_number = ""
        self.email_address = ""
        self.is_locked = False
        self.last_login_date = time.time()
        self.last_login_ip = ""
        self.credits = 0
        self.reg_remark = ""
        self.login_count = 0
        self.id: int = 0
        self.group_id = ""

    # 如下配置，需要在表格中显示的列,命名[a-z]是为了排序用：

    @annotation("用户名")
    def a_username(self):
        return self.username

    @annotation("昵称")
    def b_ni_name(self):
        return self.ni_name

    @annotation("用户组|to_user_group_name")
    def c_group_id(self):
        return self.group_id

    @annotation("手机号")
    def d_mobile_number(self):
        return self.mobile_number

    @annotation("邮箱地址")
    def e_email_address(self):
        return self.email_address

    @annotation("是否锁定|to_bool_name")
    def f_is_locked(self):
        return self.is_locked

    @annotation("职分")
    def g_credits(self):
        return self.credits

    @annotation("最后登录时间")
    def h_last_login_date(self):
        return self.last_login_date

    @annotation("最后登录IP")
    def i_last_login_ip(self):
        return self.last_login_ip

    @annotation("登录次数")
    def j_login_count(self):
        return self.login_count

    @annotation("备注")
    def k_reg_remark(self):
        return self.reg_remark

    @annotation("ID")
    def l_id(self):
        return self.id

    @annotation("注册时间")
    def n_add_time(self):
        return self.add_time
