from bll.bll_base import BllBase
from entity.news_class_model import NewsClassModel


class NewsClass(BllBase[NewsClassModel]):
    def new_instance(self) -> NewsClassModel:
        return NewsClassModel()

