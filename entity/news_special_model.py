from eb_utils import random_int
from entity.entity_base import ModelBase, annotation


class NewsSpecialModel(ModelBase):
    def __init__(self):
        super().__init__()
        self.special_nane: str = ""
        self.sort_id: int = 0
        self.parent_id: str = ""
        self.info: str = ""
        self.seo_title: str = ""
        self.seo_keyword: str = ""
        self.seo_description: str = ""
        self.hits: int = 0
        self.user_id: str = ""
        self.special_temp_id: str = ""
        self.is_good: bool = False
        self.content_ids: list[str] = []
        

    @annotation("日志标题")
    def a_user_name(self):
        return self.title
