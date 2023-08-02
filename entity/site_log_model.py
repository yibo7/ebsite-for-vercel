from entity.entity_base import ModelBase, annotation


class SiteLogModel(ModelBase):
    def __init__(self):
        super().__init__()
        self.title: str = ""
        self.description: str = ""
        self.ip_addr: str = ""
        self.url: str = ""
        self.user_id: str = ""
        self.user_name: str = ""
        self.ni_name: str = ""

    @annotation("日志标题")
    def a_user_name(self):
        return self.title

    @annotation("日志内容")
    def b_description(self):
        return self.description

    @annotation("用户")
    def c_user_name(self):
        return self.user_name

    @annotation("昵称")
    def d_ni_name(self):
        return self.ni_name

    @annotation("IP地址")
    def c_ip_addr(self):
        return self.ip_addr

    @annotation("来源")
    def d_url(self):
        return self.url

    @annotation("生成时间")
    def f_add_time(self):
        return self.add_time