from eb_event import content_ev


def init_triggers():
    content_ev.event += test_ddd


def test_ddd(data):
    print(f'收到消息：{data}')
    data['name'] = '修改后的名称'
