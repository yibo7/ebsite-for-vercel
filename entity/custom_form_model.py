from entity.entity_base import ModelBase, annotation


class CustomFormModel(ModelBase):
    def __init__(self):
        super().__init__()
        self.name: str = ""
        # self.table_name: str = ""
        self.fields: list[dict] = []  # [{'name': '', 'show_name': ''}]
        self.open_safe_code = True
        self.max_len: int = 100

    @annotation("表单名称")
    def a_name(self):
        return self.name

    @annotation("表单ID")
    def b_data_id(self):
        return f"f_{self._id}"
    @annotation("是否开启验证码")
    def b_open_safe_code(self):
        return '是' if self.open_safe_code else '否'

    @annotation("字段最大长度")
    def c_max_len(self):
        return self.max_len

    @annotation("字段数")
    def d_fields_len(self):
        return len(self.fields)

    # @annotation("示例代码")
    # def d_post_url(self):
    #     return f'/api/custom_form?key={self._id}'

    @annotation("添加时间|to_time_name")
    def e_add_time(self):
        return self.add_time
