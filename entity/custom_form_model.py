from entity.entity_base import ModelBase, annotation


class CustomFormModel(ModelBase):
    def __init__(self):
        super().__init__()
        self.name: str = ""
        self.table_name: str = ""
        self.form_ids: list[{}] = []  # {'form_id': '', 'show_name': ''}

    @annotation("日志标题")
    def a_user_name(self):
        return self.name
