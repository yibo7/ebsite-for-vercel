from bll.bll_base import BllBase
from entity.news_content_model import NewsContentModel


class NewsContent(BllBase[NewsContentModel]):
    def new_instance(self) -> NewsContentModel:
        return NewsContentModel()

