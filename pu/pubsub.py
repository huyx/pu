# -*- coding: utf-8 -*-
'''事件订阅管理

功能：

- 频道支持通配符: * ?
- 支持优先级，数值越低优先级越高，优先级可以为负数，缺省优先级为 0
- 允许终止后续消息处理: raise PubSub.Stop
'''
from collections import defaultdict
import fnmatch
import logging
from operator import itemgetter
import re


logger = logging.getLogger(__name__)


def format_channels(channels, count=5):
    if len(channels) < count:
        return channels
    omitted = '...({})...'.format(len(channels) - count)
    return channels[:count] + (omitted,)


class PubSub(object):
    class Stop(Exception):
        pass

    def __init__(self):
        # 保存订阅关系
        self.channel_handlers = defaultdict(list)
        self.pattern_handlers = defaultdict(list)

        # 保存 handler 到 channel 的反向引用，用在取消订阅的时候
        self.handler_channels = defaultdict(list)
        self.handler_patterns = defaultdict(list)

    def subscribe(self, handler, *channels, priority=0):
        logger.info('subscribe({}, {}, {})'.format(handler.__qualname__, priority, format_channels(channels)))

        handler_info = (handler, priority)

        for channel in channels:
            self.channel_handlers[channel].append(handler_info)
            self.handler_channels[handler_info].append(channel)

    def psubscribe(self, handler, *patterns, priority=0):
        logger.info('psubscribe({}, {}, {})'.format(handler.__qualname__, priority, format_channels(patterns)))

        handler_info = (handler, priority)

        # 编译要订阅的模板
        patterns = [re.compile(fnmatch.translate(pattern)) for pattern in patterns]

        for pattern in patterns:
            self.pattern_handlers[pattern].append(handler_info)
            self.handler_patterns[handler_info].append(pattern)

    def unsubscribe(self, handler, *channels, priority=0):
        '''取消订阅，channels 为空时表示取消所有 handler 的订阅
        '''
        handler_info = (handler, priority)

        if not channels:
            channels = tuple(self.handler_channels[handler_info])

        logger.info('unsubscribe({}, {}, {})'.format(handler.__qualname__, priority, format_channels(channels)))

        for channel in channels:
            try:
                self.channel_handlers[channel].remove(handler_info)
                self.handler_channels[handler_info].remove(channel)
            except KeyError:
                logger.warning('取消事件注册失败: {} {}'.format(channel, handler_info))
            else:
                # 清理空的列表项
                if not self.channel_handlers[channel]:
                    del self.channel_handlers[channel]

        # 清理空的列表项，以免 handler 被占用导致资源泄漏
        if not self.handler_channels[handler_info]:
            del self.handler_channels[handler_info]

    def punsubscribe(self, handler, *patterns, priority=0):
        '''取消订阅，patterns 为空时表示取消所有 handler 的订阅
        '''
        handler_info = (handler, priority)

        if patterns:
            # 编译要取消订阅的模板
            patterns = tuple(re.compile(fnmatch.translate(pattern)) for pattern in patterns)
        else:
            patterns = tuple(self.handler_patterns[handler_info])

        logger.info('punsubscribe({}, {}, {})'.format(handler.__qualname__, priority, format_channels(patterns)))

        for pattern in patterns:
            try:
                self.pattern_handlers[pattern].remove(handler_info)
                self.handler_patterns[handler_info].remove(pattern)
            except KeyError:
                logger.warning('取消事件注册失败: {} {}'.format(pattern, handler_info))
            else:
                # 清理空的列表项
                if not self.pattern_handlers[pattern]:
                    del self.pattern_handlers[pattern]

        # 清理空的列表项，以免 handler 被占用导致资源泄漏
        if not self.handler_patterns[handler_info]:
            del self.handler_patterns[handler_info]

    def publish(self, channel, message, sender=None):
        handler_infos = self.channel_handlers[channel].copy()

        pattern_handlers = self.pattern_handlers
        for pattern in pattern_handlers:
            if pattern.match(channel):
                handler_infos.extend(pattern_handlers[pattern])

        # 按优先级排序
        handler_infos = sorted(handler_infos, key=itemgetter(1))
        handlers = (handler for handler, _ in handler_infos)

        count = 0

        for handler in handlers:
            try:
                handler(channel, message, sender)
            except PubSub.Stop:
                break
            except Exception as e:
                logger.exception('进行消息处理 {}({}, {}, {}) 时产生异常: {}'.format(
                    handler, channel, message, sender, e))
            else:
                count += 1

        return count


pubsub = PubSub()


if __name__ == '__main__':
    from functools import partial

    pubsub.subscribe(partial(print, 'subscribe'), 'comp.learn', 'comp.python', priority=-9)
    pubsub.psubscribe(partial(print, 'psubscribe'), 'comp.*')

    pubsub.publish('comp.python', 'Tom', 'I like python')
    pubsub.publish('comp.c', 'Bob', 'I like c')
