# -*- coding: utf-8 -*-
import asyncio
import logging


logger = logging.getLogger(__name__)


class Client:
    def __init__(self, protocol_factory, loop=None):
        self.protocol_factory = protocol_factory
        self.loop = loop or asyncio.get_event_loop()

    @asyncio.coroutine
    def connect(self, host, port):
        self.host = host
        self.port = port

        yield from self._connect()

    @asyncio.coroutine
    def _connect(self):
        logger.info('连接 %s:%d', self.host, self.port)

        result = yield from self.loop.create_connection(
            self.protocol_factory, self.host, self.port)
        return result


class ReconnectingClient(Client):
    def __init__(self, protocol_factory, retry_delay=5, loop=None):
        super().__init__(protocol_factory, loop)

        self.retry_delay = retry_delay

    @asyncio.coroutine
    def _connect(self, delay=0):
        yield from asyncio.sleep(delay)

        while True:
            try:
                # create_connection 返回 transport, protocol
                _, protocol = yield from super()._connect()
                self._replace_connection_lost(protocol)
                break
            except Exception as e:
                logger.warning('连接 %s:%d 失败: %s', self.host, self.port, e)
                yield from asyncio.sleep(self.retry_delay)

    def _replace_connection_lost(self, protocol):
        # 避免重复替换 connection_lost 方法
        if hasattr(protocol, '_orig_connection_lost'):
            return

        protocol._orig_connection_lost = protocol.connection_lost

        def connection_lost(exc):
            logger.info('连接断开，重新连接: %s', exc)
            protocol._orig_connection_lost(exc)
            asyncio.async(self._connect(self.retry_delay))

        protocol.connection_lost = connection_lost


if __name__ == '__main__':
    import sys

    logging.basicConfig(level='DEBUG')

    loop = asyncio.get_event_loop()

    if '-r' in sys.argv:
        client = ReconnectingClient(asyncio.Protocol)
    else:
        client = Client(asyncio.Protocol)

    loop.run_until_complete(client.connect('127.0.0.1', 9999))

    logger.info('连接完成，可以做自己的事了.')

    loop.run_forever()
