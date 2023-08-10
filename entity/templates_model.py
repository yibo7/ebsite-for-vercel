from eb_utils import random_int
from entity.entity_base import ModelBase, annotation


class TemplatesModel(ModelBase):
    def __init__(self):
        super().__init__()
        self.name: str = ""
        self.temp_code: str = ""
        self.temp_type: int = 0  # 1.class_temp 2.content_temp 3.special_temp
        self.temp_model: int = 1  # 1.online，2.file
        self.file_path: str = ""

    @annotation("模板名称")
    def a_name(self):
        return self.name

    @annotation("模板类型")
    def b_temp_model(self):
        return '在线模板' if self.temp_model==1 else '指定文件'

    @annotation("添加时间|to_time_name")
    def c_add_time(self):
        return self.add_time