from bll.bll_base import BllBase
from entity.news_special_model import NewsSpecialModel
from entity.templates_model import TemplatesModel


class Templates(BllBase[TemplatesModel]):
    def new_instance(self) -> TemplatesModel:
        return TemplatesModel()

