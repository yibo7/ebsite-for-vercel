# from pydantic import BaseModel
# from werkzeug.security import generate_password_hash, check_password_hash
#
# from db_utils import redis_utils
# from entity.entity_base import EntityBase
# from entity.user_token import UserToken
#
#
#
# class AdminUser(EntityBase[UserToken]):
#     def __init__(self):
#         super().__init__()
#         self.user_name = ""
#         self.user_pass = ""
#         self.user_status = 0
#         self.role_id = 0
#         self.role_name = ""
#         self.real_name = ""
#         self.user_email = ""
#         self.mobile_number = ""
#
#     def add_default(self):
#         if not self.exist_table():
#             self.user_name = "admin"
#             self.user_pass = generate_password_hash("222222")
#             self.user_status = 1
#             self.role_id = 1
#             self.role_name = "超级管理员"
#             self.real_name = "创建人"
#             self.add()
#
#     def get_by_name(self, name: str):
#         return self.find_one_by_where({"user_name": name})
#
#     @staticmethod
#     def check_pass(pass_1, pass_2):
#         """
#         验证用户密码是否正确
#         :param pass_2:
#         :param pass_1:
#         :return:
#         """
#         return check_password_hash(pass_1, pass_2)
#
#     def login(self, user_name, pass_word):
#         user = self.get_by_name(user_name)
#         is_sucessfull = False
#         msg = "未知错误"
#         if user:
#             pass_1 = user["user_pass"]
#             is_sucessfull = self.check_pass(pass_1, pass_word)
#             if is_sucessfull:
#                 utk = UserToken(user["_id"], user["user_name"], user["real_name"], user['role_id'], user['role_name'])
#                 msg = redis_utils.set_ex_hours(utk, 24)
#             else:
#                 msg = "用户名或密码错误"
#         else:
#             msg = "用户名不存在或密码错误"
#         return [is_sucessfull, msg]
#
#
