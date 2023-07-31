# import time
#
# from entity.entity_base import EntityBase
#
#
# class User(EntityBase):
#     def __init__(self):
#         super().__init__()
#         self.username = ""
#         self.password = ""
#         self.mobile_number = ""
#         self.email_address = ""
#         self.is_locked = False
#         self.last_login_date = time.time()
#         self.last_login_ip = ""
#         self.credits = 0
#         self.ni_name = ""
#         self.reg_remark = ""
#         self.group_id = ""
#         self.login_count = 0
#         self.id = self.get_int_id()
#
#     def exist_name(self, name: str) -> bool:
#         return self.find_one_by_where({'username': name})
#
#     def exist_mobile(self, mobile: str) -> bool:
#         return self.find_one_by_where({'mobile_number': mobile})
#
#     def exist_email(self, email: str) -> bool:
#         return self.find_one_by_where({'email_address': email})
#
#     def add_update(self, model: dict):
#
#         u_name = model.get('username')
#         if not u_name or self.exist_name(u_name):
#             return False, '账号已存在或不能为空'
#
#         email = model.get('email_address')
#         if not email or self.exist_email(email):
#             return False, 'EMAIL已存在或不能为空'
#
#         mobile = model.get('mobile_number')
#         if not mobile or self.exist_name(mobile):
#             return False, '手机号已存在或不能为空'
#
