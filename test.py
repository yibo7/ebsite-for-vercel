from unittest import TestCase


class testCode(TestCase):
    def testList(self):
        int_id = [1, 2, 3, 5, 6, 8, 9, 10]
        str_id = ['2', '3']

        int_id = [x for x in int_id if str(x) not in str_id]
        print('结果：')
        print(int_id)

    def testModelToDic(self):
        from entity.news_content_model import NewsContentModel
        model = NewsContentModel()
        dic_f = model.__dict__
        print(dic_f)
