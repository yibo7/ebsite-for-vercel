from bll.bll_base import BllBase
from entity.news_special_model import NewsSpecialModel
from entity.templates_model import TemplatesModel


class Templates(BllBase[TemplatesModel]):
    def new_instance(self) -> TemplatesModel:
        model = TemplatesModel()
        if self.temp_type == 1:
            model.file_path = 'list.html'
        elif self.temp_type == 2:
            model.file_path = 'content.html'
        elif self.temp_type == 3:
            model.file_path = 'special.html'
        return model

    def __init__(self, temp_type: int):
        super().__init__()
        self.temp_type = temp_type # 1.class_temp 2.content_temp 3.special_temp

    def get_templates(self) -> list[TemplatesModel]:
        s_where = {"temp_type": self.temp_type}
        return self.find_list_by_where(s_where)

