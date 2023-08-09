from entity.entity_base import ModelBase, annotation


class CustomFormModel(ModelBase):
    def __init__(self):
        super().__init__()
        self.name: str = ""
        # self.table_name: str = ""
        # self.form_fields: list[{}] = []  # [{'form_id': '', 'show_name': ''}]
        self.form_fields: str = ''
        self.id: int = 0

    @annotation("表单名称")
    def a_user_name(self):
        return self.name

    @annotation("是否已配置字段")
    def b_form_ids(self):
        return '是' if len(self.form_fields)>0 else '否'

    @annotation("提交地址")
    def c_post_url(self):
        return f'/api/custom_form?key={self._id}'

    @annotation("添加时间|to_time_name")
    def d_form_ids(self):
        return self.add_time
