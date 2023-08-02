"""
Event-driven framework of Binance Tradingview Webhook Bot
"""
import sys
from collections import defaultdict
from queue import Empty, Queue
from threading import Thread
from time import sleep
from typing import Any, Callable, List

EVENT_TIMER = "eTimer"
EVENT_SIGNAL = "eSignal"


class Event:
    """
    Event object consists of a type string which is used
    by event engine for distributing event, and a data
    object which contains the real data.
    """

    def __init__(self, type: str, data: Any = None):
        """"""
        self.type: str = type
        self.data: Any = data


# Defines handler function to be used in event engine.
HandlerType = Callable[[Event], None]


class EventEngine:
    """
    将分发数据给已经注册的事件处理程序，并且还可以使用定时器模式
    """

    def __init__(self, interval: int = 1):
        """
        interval：定时间隔，如果未指定间隔，定时器事件默认每 1 秒生成一次.
        """
        self._interval: int = interval
        self._queue: Queue = Queue()
        self._active: bool = False
        self._thread: Thread = Thread(target=self._run)
        self._timer: Thread = Thread(target=self._run_timer)
        self._handlers: defaultdict = defaultdict(list)
        self._general_handlers: List = []

    def _run(self) -> None:
        """
        Get event from queue and then process it.
        """
        while self._active:
            try:
                event = self._queue.get(block=True, timeout=1)
                self._process(event)
            except Empty:
                pass

    def _process(self, event: Event) -> None:
        """
        首先将事件分发给那些注册监听的处理程序到这种类型。
        然后将事件分发给那些监听的通用处理程序
        到所有类型。
        """
        try:
            if event.type in self._handlers:
                [handler(event) for handler in self._handlers[event.type]]

            if self._general_handlers:
                [handler(event) for handler in self._general_handlers]
        except Exception:
            et, ev, tb = sys.exc_info()
            sys.excepthook(et, ev, tb)

    def _run_timer(self) -> None:
        """
        Sleep by interval second(s) and then generate a timer event.
        """
        while self._active:
            sleep(self._interval)
            event = Event(EVENT_TIMER)
            self.put(event)
            # print('ffffff')

    def start(self) -> None:
        """
        按间隔秒睡眠，然后生成计时器事件
        Start event engine to process events and generate timer events.
        """
        self._active = True
        self._thread.start()
        self._timer.start()

    def stop(self) -> None:
        """
        Stop event engine.
        """
        self._active = False
        self._timer.join()
        self._thread.join()

    def put(self, event: Event) -> None:
        """
        Put an event object into event queue.
        """
        self._queue.put(event)

    def register(self, type: str, handler: HandlerType) -> None:
        """
        Register a new handler function for a specific event type. Every
        function can only be registered once for each event type.
        为特定事件类型注册一个新的处理函数。每一个每个事件类型只能注册一次函数。
        """
        handler_list = self._handlers[type]
        if handler not in handler_list:
            handler_list.append(handler)

    def unregister(self, type: str, handler: HandlerType) -> None:
        """
        Unregister an existing handler function from event engine.
        """
        handler_list = self._handlers[type]

        if handler in handler_list:
            handler_list.remove(handler)

        if not handler_list:
            self._handlers.pop(type)

    def register_general(self, handler: HandlerType) -> None:
        """
        Register a new handler function for all event types. Every
        function can only be registered once for each event type.
        为所有事件类型注册一个新的处理函数。每一个每个事件类型只能注册一次函数。
        """
        if handler not in self._general_handlers:
            self._general_handlers.append(handler)

    def unregister_general(self, handler: HandlerType) -> None:
        """
        Unregister an existing general handler function.
        """
        if handler in self._general_handlers:
            self._general_handlers.remove(handler)