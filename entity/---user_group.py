#
# # from entity.entity_base import EntityBase
# from entity.site_settings import get_settings
#
#
# class UserGroup(EntityBase):
#     def __init__(self):
#         super().__init__()
#         self.name = ""
#
#     def add_default(self):
#         if not self.exist_table():
#             self.name = "普通会员"
#             _id = self.add()
#             st = get_settings()
#             st.reg_group_id = str(_id)
#             st.save()
#
#     def exist_name(self, name: str) -> bool:
#         return self.find_one_by_where({'name': name})
#
#
