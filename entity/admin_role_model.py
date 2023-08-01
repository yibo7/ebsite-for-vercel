from entity.entity_base import ModelBase, annotation


class AdminRoleModel(ModelBase):
    def __init__(self):
        super().__init__()
        self.name = ""
        self.info = ""
        self.pos_id = []

    @annotation("角色名称")
    def a_name(self):
        return self.name

    @annotation("权限数量")
    def a_pos_id(self):
        return f'{len(self.pos_id)}个'

    @annotation("角色说明")
    def b_info(self):
        return self.info
