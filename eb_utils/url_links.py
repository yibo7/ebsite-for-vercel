def get_class_url(c_id: int, page_code: int = 1):
    return f'/c{c_id}p{page_code}.html'


def get_content_url(a_id: int):
    return f'/a{a_id}.html'


def get_special_url(c_id: int, page_code: int = 1):
    return f'/s{c_id}p{page_code}.html'
