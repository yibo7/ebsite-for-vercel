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
        self.rand_num: int = random_int(1,100)
        self.is_good: bool = False
        self.content_temp_id: str = ""
        self.id: int = 0

    @annotation("标题")
    def a_title(self):
        return self.title

    @annotation("分类名称")
    def b_class_nane(self):
        return self.class_nane

    @annotation("访问次数")
    def c_hits(self):
        return self.hits

    @annotation("添加人")
    def d_user_name(self):
        return self.user_name

    @annotation("是否推荐|to_bool_name")
    def e_is_good(self):
        return self.is_good

    @annotation("添加时间|to_time_name")
    def f_add_time(self):
        return self.add_time

