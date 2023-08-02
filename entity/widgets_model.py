from eb_utils import random_int
from entity.entity_base import ModelBase, annotation


class WidgetsModel(ModelBase):
    def __init__(self):
        super().__init__()
        self.name: str = ""
        self.where_query: str = ""
        self.temp_code: str = ""
        self.temp_type: int = 0  # 1.class_data 2.content_data 3.special_data 4.user_data

    @annotation("日志标题")
    def a_user_name(self):
        return self.title
