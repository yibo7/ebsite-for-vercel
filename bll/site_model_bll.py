from bll.bll_base import BllBase
from entity.news_special_model import NewsSpecialModel
from entity.site_model import SiteModel
from entity.templates_model import TemplatesModel


class SiteModelBll(BllBase[SiteModel]):
    def new_instance(self) -> SiteModel:
        model = SiteModel()
        return model


