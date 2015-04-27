# -*- coding: utf-8 -*-
import asyncio


__all__ = ['Timer']


class Timer:
    __timer = None

    def __init__(self, callback=None, loop=None):
        self.callback = callback or self.timeout
        self.loop = loop or asyncio.get_event_loop()

    def set_timeout(self, delay):
        assert not self.__timer

        self.__timer = self.loop.call_later(delay, self._timeout)

    def cancel_timeout(self):
        if self.__timer:
            self.__timer.cancel()
            self.__timer = None

    def reset_timeout(self, delay):
        self.cancel_timeout()
        self.set_timeout(delay)

    def _timeout(self):
        self.__timer = None

        self.callback()

    def timeout(self):
        raise NotImplementedError


if __name__ == '__main__':
    import time
    start = time.time()

    now = lambda : round(time.time() - start, 6)

    loop = asyncio.get_event_loop()

    def timeout():
        print(now(), '时间到')
        loop.stop()

    def delay():
        print(now(), '推迟到 3 秒后')
        timer.reset_timeout(3)

    timer = Timer(timeout)
    print(now(), '启动 3 秒定时')
    timer.set_timeout(3)
    loop.call_later(2, delay)

    loop.run_forever()
