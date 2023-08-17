from bll.bll_base import BllBase
from entity.custom_form_model import CustomFormModel


class CustomForm(BllBase[CustomFormModel]):
    def new_instance(self) -> CustomFormModel:
        return CustomFormModel()

    # def get_table_header(self,model: CustomFormModel):
    #     model.fields




    def save_fields(self, model: CustomFormModel, field_dict: dict):
        exists = any(f_m.get('name') == field_dict.get('name') for f_m in model.fields)
        if not exists:
            model.fields.append(field_dict)
            self.save(model)
            return True
        return False

    def del_field(self, _id: str, field_name):
        model = self.find_one_by_id(_id)
        new_list = [item for item in model.fields if item.get('name') != field_name]
        model.fields = new_list
        self.save(model)

    def get_demo_tem(self, model: CustomFormModel):
        demo_tem = [f'<form id="f_{model._id}" onsubmit="return on_custom_form(this)" method="post" >\r\n']

        for item in model.fields:
            demo_tem.append('<div class="mb-3">\r\n')
            demo_tem.append(f'  <label>{item.get("show_name")}</label>\r\n')
            demo_tem.append(f'  <input name="{item.get("name")}" minlength="1"  class="form-control" required>\r\n')
            demo_tem.append('</div>\r\n')
        if model.open_safe_code:
            demo_tem.append('<div class="row">\r\n')
            demo_tem.append('   <label class="form-label" >验证码</label>\r\n')
            demo_tem.append('   <div class="btn-group safe_code_img">\r\n')
            demo_tem.append('       <input type="text" name="safe_code"  style="max-width:100px" class="form-control" title="验证码为4个字符" pattern=".{4}" required/>\r\n')
            demo_tem.append('       <img onClick="this.src+=Math.random()" src="/imgcode?" />\r\n')
            demo_tem.append('   </div>\r\n')
            demo_tem.append('</div>\r\n')

        demo_tem.append('<button class="btn btn-primary mb-3 mt-3" type="submit">   提交   </button>\r\n')
        demo_tem.append('</form>\r\n')
        return ''.join(demo_tem)
