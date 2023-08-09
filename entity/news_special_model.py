from eb_utils import random_int
from entity.entity_base import ModelBase, annotation


class NewsSpecialModel(ModelBase):
    def __init__(self):
        super().__init__()
        self.name: str = ""
        self.order_id: int = 0
        self.parent_id: str = ""
        self.info: str = ""
        self.seo_title: str = ""
        self.seo_keyword: str = ""
        self.seo_description: str = ""
        self.hits: int = 0
        self.user_id: str = ""
        self.temp_id: str = ""
        self.is_good: bool = False
        self.content_ids: list[str] = []
        self.id: int = 0

    @annotation("专题名称")
    def a_name(self):
        return self.name

    @annotation("排序权重")
    def b_order_id(self):
        return self.order_id

    @annotation("是否推荐|to_bool_name")
    def c_is_good(self):
        return self.is_good

    @annotation("添加时间|to_time_name")
    def d_add_time(self):
        return self.add_time