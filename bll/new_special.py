from bll.bll_base import BllBase
from entity.news_special_model import NewsSpecialModel


class NewsSpecial(BllBase[NewsSpecialModel]):
    def new_instance(self) -> NewsSpecialModel:
        return NewsSpecialModel()

