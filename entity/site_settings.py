from dataclasses import dataclass

from db_utils import redis_utils

key_settings = "settings"


@dataclass
class SiteSettings:
    site_name: str
    err_login_lock: int
    reg_group_id: str
    is_open_safe_code: bool

    def save(self):
        redis_utils.set_obj(self, 0, key_settings)


def SiteSettings_Default():
    return SiteSettings('SiteName', 3, '', True)


def get_settings() -> SiteSettings:
    v: SiteSettings = redis_utils.get_obj(key_settings)
    return v if v else SiteSettings_Default()
