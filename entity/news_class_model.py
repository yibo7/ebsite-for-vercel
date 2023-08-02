from entity.entity_base import ModelBase, annotation


class NewsClassModel(ModelBase):
    def __init__(self):
        super().__init__()
        self.class_nane: str = ""
        self.sort_id: int = 0
        self.parent_id: str = ""
        self.info: str = ""
        self.seo_title: str = ""
        self.seo_keyword: str = ""
        self.seo_description: str = ""
        self.hits: int = 0
        self.user_id: str = ""
        self.user_group_ids: list[str] = []   # allow user group ids
        self.class_temp_id: str = ""
        self.content_temp_id: str = ""



    @annotation("日志标题")
    def a_user_name(self):
        return self.title
