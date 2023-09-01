import time

from entity.entity_base import ModelBase, annotation


class FileModel(ModelBase):
    def __init__(self):
        super().__init__()
        # self.name = ""
        self.original_name = ""
        self.size = 0
        self.type = ""
        self.mimetype = ""
        self.url = ""
        self.content = None
        self.id: int = 0

    # 如下配置，需要在表格中显示的列,命名[a-z]是为了排序用：

    @annotation("文件名称")
    def a_name(self):
        return self.name

    @annotation("原始名称")
    def b_original_name(self):
        return self.original_name

    @annotation("文件大小")
    def c_size(self):
        return self.size

    @annotation("文件类型")
    def d_type(self):
        return self.type

    @annotation("文件URL")
    def e_url(self):
        return self.url

    @annotation("ID号")
    def f_url(self):
        return self.id

    @annotation("上传时间")
    def n_add_time(self):
        return self.add_time
