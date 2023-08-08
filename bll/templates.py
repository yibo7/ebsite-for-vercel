from bll.bll_base import BllBase
from entity.news_special_model import NewsSpecialModel
from entity.templates_model import TemplatesModel


class Templates(BllBase[TemplatesModel]):
    def new_instance(self) -> TemplatesModel:
        return TemplatesModel()

    def __init__(self, temp_type: int):
        super().__init__()
        self.temp_type = temp_type # 1.class_temp 2.content_temp 3.special_temp

    def get_templates(self) -> list[TemplatesModel]:
        s_where = {"temp_type": self.temp_type}
        return self.find_list_by_where(s_where)

