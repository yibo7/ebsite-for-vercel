from bll.bll_base import BllBase
from eb_utils import http_helper
from entity.site_log_model import SiteLogModel


class SiteLog(BllBase[SiteLogModel]):
    def new_instance(self) -> SiteLogModel:
        return SiteLogModel()

    # def add_log(self, title: str,content: str):
    #     model = self.new_instance()
    #     model.title = title
    #     model.description = content
    #     model.url = http_helper.get_url_full()
    #     model.ip_addr = http_helper.get_ip()
    #
    #     self.add(model)
