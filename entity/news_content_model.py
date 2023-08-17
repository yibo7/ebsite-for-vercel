from typing import Any

from eb_utils import random_int, url_links
from entity.entity_base import ModelBase, annotation


class NewsContentModel(ModelBase):
    def __init__(self):
        super().__init__()
        self.title: str = ""
        self.info: str = ""
        self.small_pic = ""
        self.class_name: str = ""
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
        self.rand_num: int = random_int(1, 100)
        self.is_good: bool = False
        # self.content_temp_id: str = ""
        self.id: int = 0
        self.column_1: Any = None
        self.column_2: Any = None
        self.column_3: Any = None
        self.column_4: Any = None
        self.column_5: Any = None
        self.column_6: Any = None
        self.column_8: Any = None
        self.column_9: Any = None
        self.column_10: Any = None
        self.column_11: Any = None
        self.column_12: Any = None
        self.column_13: Any = None
        self.column_14: Any = None
        self.column_15: Any = None
        self.column_16: Any = None
        self.column_17: Any = None
        self.column_18: Any = None
        self.column_19: Any = None
        self.column_20: Any = None
        self.column_21: Any = None

    def get_url(self):
        return url_links.get_content_url(self.id)

    @annotation("文章标题")
    def a_title(self):
        return f'<a href="{self.get_url()}" target=_blank >{self.title}</a>'

    @annotation("文章ID")
    def b_a_id(self):
        return self.id

    @annotation("分类名称")
    def b_class_name(self):
        return self.class_name

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
