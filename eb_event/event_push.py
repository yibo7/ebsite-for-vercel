class EbEvent:
    def __init__(self):
        self.handlers = []

    def __iadd__(self, handler):
        self.handlers.append(handler)
        return self

    def __isub__(self, handler):
        self.handlers.remove(handler)
        return self

    def __call__(self, *args, **kwargs):
        for handler in self.handlers:
            handler(*args, **kwargs)


class EventHandler:
    def __init__(self):
        self.event = EbEvent()

    def to_do(self, data):
        self.event(data)


# def event_handler(data):
#     print("接收到!")
#     print(data)
#     data['name'] = '小明'


# publisher = EventHandler()
# publisher.event += event_handler
#
# data = {'name': 'cqs'}
# publisher.to_do(data)
# print(data)