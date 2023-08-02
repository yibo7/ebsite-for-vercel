from bll.bll_base import BllBase
from entity.custom_form_model import CustomFormModel


class CustomForm(BllBase[CustomFormModel]):
    def new_instance(self) -> CustomFormModel:
        return CustomFormModel()

