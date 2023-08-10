class WebPaths(object):
    ADMIN_PATH = "/admin/"
    ADMIN_LOGIN = "/login_ad"
    ADMIN_INDEX = f"{ADMIN_PATH}index"
    LOGIN_URL = "/login"
    USER_PATH = "/user/"
    USER_INDEX = f"{USER_PATH}index"
    API_PATH = "/api/"

    @staticmethod
    def get_admin_path(temp_name: str):
        return f"admin/{temp_name}"


class SiteConstant(object):
    COOKIE_AD_TOKEN_KEY = "ua_key"
    PAGE_SIZE_AD = 30
