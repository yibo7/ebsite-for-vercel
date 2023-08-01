from entity.entity_base import ModelBase, annotation


class AdminMenuModel(ModelBase):
    def __init__(self):
        super().__init__()
        self.menu_name: str = ""
        self.image_url: str = ""
        self.order_id: int = 0
        self.parent_id: str = ""
        self.page_url: str = ""
        self.is_menu: bool = True

    @annotation("菜单名称")
    def a_username(self):
        return self.menu_name

    @annotation("是否菜单|to_bool_name")
    def b_is_menu(self):
        return self.is_menu
