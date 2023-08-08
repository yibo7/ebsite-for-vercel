from bll.bll_base import BllBase
from entity.widgets_model import WidgetsModel


class Widgets(BllBase[WidgetsModel]):
    def new_instance(self) -> WidgetsModel:
        return WidgetsModel()

