from entity.entity_base import ModelBase, annotation


class WidgetsModel(ModelBase):
    def __init__(self):
        super().__init__()
        self.name: str = ""
        self.order_by: str = "_id"
        self.order_by_desc: str = "DESC"
        self.limit: int = 10
        self.where_query: str = ""
        self.temp_code: str = ""
        self.info: str = ""
        self.temp_type: int = 0  # 1.class_data 2.content_data 3.special_data 4.user_data 5.text 6.html
        self.user_id: str = ""

    @annotation("部件名称")
    def a_name(self):
        return self.name

    @annotation("部件类型|widget_type_name")
    def b_temp_type(self):
        return self.temp_type

    @annotation("添加时间|to_time_name")
    def d_add_time(self):
        return self.add_time
