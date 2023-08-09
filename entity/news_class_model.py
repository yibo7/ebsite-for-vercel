from entity.entity_base import ModelBase, annotation


class NewsClassModel(ModelBase):
    def __init__(self):
        super().__init__()
        self.class_name: str = ""
        self.order_id: int = 0
        self.parent_id: str = ""
        self.info: str = ""
        self.seo_title: str = ""
        self.seo_keyword: str = ""
        self.seo_description: str = ""
        self.hits: int = 0
        self.user_id: str = ""
        self.user_group_ids: list[str] = []  # allow user group ids
        self.class_temp_id: str = ""
        self.content_temp_id: str = ""
        self.id: int = 0

    @annotation("分类名称")
    def a_class_name(self):
        return self.class_name

    @annotation("排序ID")
    def b_order_id(self):
        return self.order_id

    @annotation("添加时间|to_time_name")
    def c_add_time(self):
        return self.add_time
