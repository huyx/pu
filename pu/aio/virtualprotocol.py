# -*- coding: utf-8 -*-
import asyncio
import logging

logging.warning('%s 已经废弃，请使用 dummyprotocol.', __name__)

__all__ = ['VirtualProtocol', 'RealProtocol']

logger = logging.getLogger(__name__)


class VirtualProtocol(asyncio.Protocol):
    _real_protocol = None
    _protocol_detect_buffer = b''

    def __init__(self, factory):
        self._protocol_factories = factory._protocol_factories.copy()
        self._default_protocol_factory = factory._default_protocol_factory

    def set_real_protocol(self, protocol):
        self._real_protocol = protocol
        self._real_protocol.connection_made(self.transport)
        self.data_received = protocol.data_received
        self.connection_lost = protocol.connection_lost

    def connection_made(self, transport):
        self.transport = transport
        self.peername = '%s:%d' % transport.get_extra_info('peername')
        self.sockname = '%s:%d' % transport.get_extra_info('sockname')

        logger.debug('连接建立: 远端 %s, 本地 %s', self.peername, self.sockname)

    def connection_lost(self, exc):
        assert not self._real_protocol

        logger.debug('连接断开: %s, 远端 %s, 本地 %s', exc, self.peername, self.sockname)

    def data_received(self, data):
        assert not self._real_protocol

        data = self._protocol_detect_buffer + data

        for factory in self._protocol_factories[:]:
            result = factory.protocol_detect(data)
            if result == factory.YES:
                logger.debug('协议检测成功: %s 采用 %s 协议', self.peername, factory.__name__)
                self.set_real_protocol(factory(self))
                break
            elif result == factory.NO:
                self._protocol_factories.remove(factory)

        if not self._protocol_factories:
            if self._default_protocol_factory:
                factory = self._default_protocol_factory
                logger.info('%s 采用缺省协议: %s', self.peername, factory.__name__)
                self.set_real_protocol(factory(self))
            else:
                logger.info('不可识别的协议, 断开连接 %s: %r', self.peername, data)
                self.transport.close()
        elif self._real_protocol:
            self._real_protocol.data_received(data)
        else:
            self._protocol_detect_buffer = data


class VirtualProtocolFactory:
    def __init__(self, virtual_protocol_class=VirtualProtocol):
        self.virtual_protocol_class = virtual_protocol_class

        self._protocol_factories = []
        self._default_protocol_factory = None

    def register_protocol_factory(self, protocol_factory, default=False):
        if default:
            assert not self._default_protocol_factory
            self._default_protocol_factory = protocol_factory
        else:
            assert protocol_factory not in self._protocol_factories
            self._protocol_factories.append(protocol_factory)

    def __call__(self):
        return self.virtual_protocol_class(self)


class RealProtocol:
    NO = 'NO'
    YES = 'YES'
    NOTSURE = 'NOTSURE'

    protocol_features = []      # bytes 列表

    @classmethod
    def protocol_detect(cls, data):
        if not cls.protocol_features:
            raise RuntimeError('未指定协议特征，无法检测.')

        notsure = False
        for feature in cls.protocol_features:
            if data.startswith(feature):
                return cls.YES
            if feature.startswith(data):
                # 如果 feature 以 data 开头，说明数据不够，不足以判别
                notsure = True

        if notsure:
            return cls.NOTSURE

        return cls.NO

    def __init__(self, virtual_protocol):
        self.virtual_protocol = virtual_protocol

    def connection_made(self, transport):
        self.transport = transport
        self.peername = self.virtual_protocol.peername
        self.sockname = self.virtual_protocol.sockname

    def connection_lost(self, exc):
        logger.debug('连接断开: %s, 远端 %s, 本地 %s', exc, self.peername, self.sockname)

    def data_received(self, data):
        logger.debug('来自 %s : %r', self.peername, data)


if __name__ == '__main__':
    class PYES(RealProtocol):
        protocol_features = [b'YES']

    class PNO(RealProtocol):
        protocol_features = [b'NO']

    class PNOTSURE(RealProtocol):
        protocol_features = [b'NOTSURE']

    class PXX(RealProtocol):
        @classmethod
        def protocol_detect(cls, data):
            if len(data) < 2:
                return cls.NOTSURE
            if data[0] == data[1]:
                return cls.YES
            return cls.NO

    logging.basicConfig(level='DEBUG')

    factory = VirtualProtocolFactory()
    factory.register_protocol_factory(PYES)
    factory.register_protocol_factory(PNOTSURE)
    factory.register_protocol_factory(PNO, True)
    factory.register_protocol_factory(PXX)

    loop = asyncio.get_event_loop()
    host, port = '0.0.0.0', 9999
    loop.run_until_complete(loop.create_server(factory, host, port))
    logger.info('监听: %s:%d', host, port)
    loop.run_forever()
