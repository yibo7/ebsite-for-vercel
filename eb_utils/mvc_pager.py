from typing import List
from urllib.parse import urlencode
from urllib.parse import quote
from flask import request
from markupsafe import Markup


def pager_html_admin(count: int, page_number: int, page_size: int, prams=None):
    if prams is None:
        prams = {}
    if count > page_size:
        pg = MvcPager()
        pg.current_page = page_number
        pg.total_count = count
        pg.page_size = page_size
        pg.params = prams
        pg.ShowCodeNum = 10

        return pg.show_pages()
    return ""


class MvcPager:
    def __init__(self):
        self.show_code_num = 5
        self.params = {}
        self.current_page = 0
        self.page_size = 0
        self.total_count = 0
        self.first_page_url = ""
        self.rewrite_rule = ""

    @property
    def page_num(self) -> int:
        if self.total_count <= 0 or self.page_size <= 0:
            return 1
        else:
            return ((self.total_count + self.page_size) - 1) // self.page_size

    @property
    def current_pages(self) -> List[int]:
        arr_current_pages = []
        for k in range(self.current_page - self.show_code_num, self.current_page + self.show_code_num + 1):
            if k < 0:
                continue
            if k >= self.page_num:
                break
            arr_current_pages.append(k)
        return arr_current_pages

    @property
    def rewrite_patch_url(self) -> str:
        if not self.rewrite_rule:
            return request.path + "?p={0}"
        return self.rewrite_rule

    def build_url(self, page_number: int) -> str:
        url = ""
        if page_number > 1:
            url = self.rewrite_patch_url.format(page_number)
        else:
            if self.first_page_url:
                url = self.first_page_url
            url = self.rewrite_patch_url.format(page_number)
        if self.params:
            params = urlencode(self.params, quote_via=quote)
            url = f"{url}&{params}"
        return url

    def show_pages(self) -> str:
        sb = ["<ul class='pagination'>"]
        if self.current_page > 1:
            if self.current_page > self.show_code_num:
                sb.append(f"<li class='page-item'><a href='{self.build_url(1)}'>首页</a></li>")
            sb.append(
                f"<li class='page-item'><a class='page-link' href='{self.build_url(self.current_page - 1)}'>上一页</a></li>")

        for i in self.current_pages:
            if i + 1 == self.current_page:
                sb.append(f"<li class='page-item active'><a class='page-link' href='#'>{i + 1}</a></li>")
            else:
                sb.append(f"<li class='page-item'><a class='page-link' href='{self.build_url(i + 1)}'>{i + 1}</a></li>")

        if self.current_page < self.page_num:
            sb.append(
                f"<li class='page-item'><a class='page-link' href='{self.build_url(self.current_page + 1)}'>下一页</a></li>")
            if self.current_page < (self.page_num - self.show_code_num - 1):
                sb.append(
                    f"<li class='page-item'><a class='page-link' href='{self.build_url(self.page_num)}'>尾页</a></li>")

        sb.append("</ul>")
        return Markup("".join(sb))
