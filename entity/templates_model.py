from eb_utils import random_int
from entity.entity_base import ModelBase, annotation


class TemplatesModel(ModelBase):
    def __init__(self):
        super().__init__()
        self.name: str = ""
        self.temp_code: str = ""
        self.temp_type: int = 0  # 1.class_temp 2.content_temp 3.special_temp

    @annotation("日志标题")
    def a_user_name(self):
        return self.title
