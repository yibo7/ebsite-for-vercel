from eb_utils import random_int, url_links
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
        self.content_ids: list[int] = []
        self.id: int = 0
        self.page_size = 30

    @annotation("专题名称")
    def a_name(self):
        return f'<a href="{url_links.get_special_url(self.id)}" target=_blank >{self.name}</a>'

    @annotation("专题ID")
    def b_a_id(self):
        return self.id

    @annotation("专题数据")
    def c_id(self):
        return f'<a href="special_content_list?sid={self._id}">查看数据(<font color=red>{len(self.content_ids)}</font>)<a/>'

    @annotation("排序权重")
    def d_order_id(self):
        return self.order_id

    @annotation("是否推荐|to_bool_name")
    def e_is_good(self):
        return self.is_good

    @annotation("添加时间|to_time_name")
    def f_add_time(self):
        return self.add_time
