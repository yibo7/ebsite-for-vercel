from bll.bll_base import BllBase, T
# from entity.entity_base import EntityBase
from entity.site_settings import get_settings
from entity.user_group_model import UserGroupModel


class UserGroup(BllBase[UserGroupModel]):
    def new_instance(self) -> UserGroupModel:
        return UserGroupModel()

    def add_default(self):
        if not self.exist_table():
            model = self.new_instance()
            model.name = "普通会员"
            _id = self.add(model)
            st = get_settings()
            st.reg_group_id = str(_id)
            st.save()

    def exist_name(self, name: str) -> bool:
        return self.exist_data('name', name)
