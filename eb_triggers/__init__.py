from eb_event import content_saving, class_saving
from entity.news_class_model import NewsClassModel
from entity.news_content_model import NewsContentModel


def init_triggers():
    content_saving.event += test_content_saving
    class_saving.event += test_class_saving


def test_class_saving(model: NewsClassModel):
    # model.class_name = None # 这样可以阻止分类的保存操作
    print(f'保存分类前触发,标题:{model.class_name}')


def test_content_saving(model: NewsContentModel):
    # model.title = None # 这样可以阻止内容的保存操作
    print(f'保存内容前触发,标题:{model.title}')
