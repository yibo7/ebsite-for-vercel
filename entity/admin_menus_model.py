from entity.entity_base import ModelBase


class AdminMenuModel(ModelBase):
    def __init__(self):
        super().__init__()
        self.menu_name: str = ""
        self.image_url: str = ""
        self.order_id: int = 0
        self.parent_id: str = ""
        self.page_url: str = ""
        self.is_menu: bool = True
