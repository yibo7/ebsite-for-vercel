import json


class XsJson:
    def __init__(self, path):
        """
        :param path: json文件的路径，可以是相对路径 'data/action.json'
        """
        self.save_path = path

    def save(self, jsonobj):
        """
        将对象序列化到json文件
        :param jsonobj: 可以是列表，也可以是字典
        :return:
        """
        with open(self.save_path, 'w') as fp:
            json.dump(jsonobj, fp, indent=4)

    def load(self):
        with open(self.save_path, "r", encoding="utf-8") as fr:
            file_content = fr.read()  # data 是读取到的结果
            if len(file_content) > 1:
                return json.loads(file_content)
        return None
