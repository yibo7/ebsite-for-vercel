from eb_utils import random_int
from entity.entity_base import ModelBase, annotation


class SiteModel(ModelBase):
    def __init__(self):
        super().__init__()
        self.name: str = ""
        self.field_setting:dict = {}

    @annotation("模型名称")
    def a_name(self):
        return self.name

    @annotation("添加时间|to_time_name")
    def c_add_time(self):
        return self.add_time
