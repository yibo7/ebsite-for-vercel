from entity.entity_base import ModelBase


class UserGroupModel(ModelBase):
    def __init__(self):
        super().__init__()
        self.name = ""

    # def add_default(self):
    #     if not self.exist_table():
    #         self.name = "普通会员"
    #         _id = self.add()
    #         st = get_settings()
    #         st.reg_group_id = str(_id)
    #         st.save()
    #
    # def exist_name(self, name: str) -> bool:
    #     return self.find_one_by_where({'name': name})

    # def get_sel_items(self, sel_value: str):
    #     datas = self.find_all()
    #     items = []
    #     for item in datas:
    #         temp = SelectItem(str(item['_id']), item['name'])
    #         items.append(temp)
    #
    #     return sel_box_html(items, sel_value)
