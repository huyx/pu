# -*- coding: utf-8 -*-
class Observerable:
    '''观察者模式

    用法:

    observerable = Observerable()

    observerable.add_observer(print)

    observerable.notify_observers('hello')
    '''
    _observers = None

    def add_observer(self, observer):
        '''添加观察者（可调用）

        :param observer: 观察者
        '''
        assert callable(observer)

        if self._observers is None:
            self._observers = []

        self._observers.append(observer)

    def remove_observer(self, observer):
        '''移除观察者

        :param observer: 观察者
        '''
        assert observer in self._observers

        self._observers.remove(observer)

    def notify_observers(self, *args, **kwargs):
        '''通知观察者

        :param message: 消息
        '''
        for observer in self._observers:
            observer(*args, **kwargs)
