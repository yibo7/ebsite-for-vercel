from dataclasses import dataclass


from entity.entity_base import ModelBase, annotation


@dataclass
class FieldModel:
    name: str
    show_name: str
    control_id: str
    control_name: str
    control_size: str


class SiteModelEntity(ModelBase):
    def __init__(self):
        super().__init__()
        self.name: str = ""
        self.fields: list[dict] = []

    @annotation("模型名称")
    def a_name(self):
        return self.name

    @annotation("添加时间|to_time_name")
    def c_add_time(self):
        return self.add_time
