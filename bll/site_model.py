from bll.bll_base import BllBase
from entity.list_item import ListItem
from entity.site_model_entity import SiteModelEntity, FieldModel


class SiteModel(BllBase[SiteModelEntity]):
    def new_instance(self) -> SiteModelEntity:
        model = SiteModelEntity()
        return model

    def save_default(self, model: SiteModelEntity):
        field = FieldModel(name='title', show_name='标题', control_id='1', control_name='单行文本输入框', control_size='3' )
        model.fields.append(field.__dict__)

        field = FieldModel(name='info', show_name='内容', control_id='2', control_name='多行文本输入框',
                           control_size='5')
        model.fields.append(field.__dict__)

        self.save(model)

    def save_fields(self, model: SiteModelEntity, field_model: FieldModel):
        exists = any(f_m.get('name') == field_model.name for f_m in model.fields)
        if not exists:
            model.fields.append(field_model.__dict__)
            self.save(model)
            return True
        return False

    def del_field(self, _id: str, field_name):
        model = self.find_one_by_id(_id)
        new_list = [item for item in model.fields if item.get('name') != field_name]
        model.fields = new_list
        self.save(model)

    @staticmethod
    def get_controls() -> list[ListItem]:
        lst = [
            ListItem(value=1, name='单行文本输入框'),
            ListItem(value=2, name='多行文本输入框'),
            ListItem(value=3, name='富文本编辑框'),
            ListItem(value=4, name='数字输入框'),
            ListItem(value=5, name='单图上传控件'),
            ListItem(value=6, name='单文件上传控件')
        ]
        return lst

    @staticmethod
    def get_control_by_id(ctr_id: int) -> ListItem:
        ctrs = SiteModel.get_controls()
        result = [item for item in ctrs if item.value == ctr_id]
        return result[0] if result else None

    @staticmethod
    def get_fields() -> list[str]:
        from entity.news_content_model import NewsContentModel

        attributes = []
        model = NewsContentModel()
        dic_f = model.__dict__
        dic_f.pop('_id')
        dic_f.pop('is_good')
        dic_f.pop('id')
        dic_f.pop('rand_num')
        dic_f.pop('user_id')
        dic_f.pop('user_name')
        dic_f.pop('user_ni_name')
        dic_f.pop('favorable_num')
        dic_f.pop('comment_num')
        dic_f.pop('hits')
        dic_f.pop('seo_description')
        dic_f.pop('seo_keyword')
        dic_f.pop('seo_title')
        dic_f.pop('class_id')
        dic_f.pop('class_name')
        dic_f.pop('add_time')

        # 获取当前类的属性
        for name, value in dic_f.items():
            attributes.append(name)

        return attributes

    def get_model_temp_by_id(self, model_id: str):
        model = self.find_one_by_id(model_id)
        a_html = []
        for field in model.fields:
            control_type = int(field.get('control_id'))
            show_name = field.get('show_name')
            name = field.get('name')
            if control_type == 1:
                a_html.append('<div class="mb-3">'
                              f'<label>{show_name}</label>'
                              f'<input name="{name}" value="[[model.{name}]]" minlength="3" style="max-width:500px" class="form-control" required>'
                              '</div>')
            elif control_type == 2:
                a_html.append('<div class="mb-3">'
                              f'<label>{show_name}</label>'
                              f'<textarea name="{name}" style="max-width:500px" class="form-control" rows="4" cols="50">[[model.{name}]]</textarea>'
                              '</div>')

        s_html = ''.join(a_html)
        s_html = s_html.replace('[[', '{{').replace(']]', '}}')
        return s_html
