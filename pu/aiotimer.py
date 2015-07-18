# -*- coding: utf-8 -*-
import asyncio
import logging


logger = logging.getLogger('aiotimer')

__all__ = ['TimerManager', 'timer_manager']


class Timer:
    timer = None

    def __init__(self, timer_id, delay, callback, loop, manager=None):
        self.timer_id = timer_id or id(self)
        self.delay = delay
        self.callback = callback
        self.loop = loop
        self.manager = manager or timer_manager

    def set_timer_id(self, timer_id):
        if self.manager.get(self.timer_id) == self:
            del self.manager[self.timer_id]
        else:
            logger.warning('%s not in TimerManager', self.timer_id)
        self.manager[timer_id] = self

    def start(self):
        assert not self.timer
        self.timer = self.loop.call_later(self.delay, self.callback)

    def reset(self, delay=None):
        assert self.timer

        if delay:
            self.delay = delay

        self.timer.cancel()
        self.timer = self.loop.call_later(self.delay, self.callback)

    def stop(self):
        if self.timer:
            self.timer.cancel()
            self.clean()

    def timeout(self):
        # 注意执行顺序，callback 中可能会调用 stop
        self.clean()
        self.callback()

    def clean(self):
        self.timer = None
        self.callback = None

        if self.manager.get(self.timer_id) == self:
            del self.manager[self.timer_id]


class TimerManager(dict):
    def __init__(self, loop=None):
        self.loop = loop or asyncio.get_event_loop()

    def create(self, timer_id, delay, callback, auto_start=True, loop=None):
        assert timer_id not in self, 'timer_id 已经存在'

        timer = Timer(timer_id, delay, callback, loop or self.loop, self)

        if auto_start:
            timer.start()

        return self.setdefault(timer.timer_id, timer)


timer_manager = TimerManager()
