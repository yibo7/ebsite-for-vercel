from eb_utils import random_int
from entity.entity_base import ModelBase, annotation


class NewsContentModel(ModelBase):
    def __init__(self):
        super().__init__()
        self.title: str = ""
        self.info: str = ""
        self.small_pic = ""
        self.class_nane: str = ""
        self.class_id: str = ""
        self.seo_title: str = ""
        self.seo_keyword: str = ""
        self.seo_description: str = ""
        self.hits: int = 0
        self.comment_num: int = 0
        self.favorable_num: int = 0
        self.user_id: str = ""
        self.user_name: str = ""
        self.user_ni_name: str = ""
        # self.rand_num: int = random_int(1,100)
        self.is_good: bool = False
        self.content_temp_id: str = ""

        

    @annotation("日志标题")
    def a_user_name(self):
        return self.title
