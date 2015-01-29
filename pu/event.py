# -*- coding: utf-8 -*-
class Event(list):
    """事件订阅

    参考:

    - http://stackoverflow.com/questions/1092531/event-system-in-python/2022629#2022629
    """
    def __call__(self, *args, **kwargs):
        return [func(*args, **kwargs) for func in self]


class EventNamespace(dict):
    def event(self, name):
        if name in self:
            return self[name]
        return self.setdefault(name, Event())


event = EventNamespace().event
