# -*- coding: utf-8 -*-
import asyncio
import functools
import logging


__all__ = [
    'YES', 'NO', 'UNSURE',
    'DummyProtocolFactory',
    ]

YES = 'YES'
NO = 'NO'
UNSURE = 'UNSURE'

logger = logging.getLogger('dummyprotocol')


class DummyProtocol(asyncio.Protocol):
    _real_protocol = None
    _protocol_detect_buffer = b''

    def __init__(self, factory):
        self._protocol_factories = factory._protocol_factories.copy()
        self._default_protocol_factory = factory._default_protocol_factory

    def set_real_protocol(self, protocol):
        # 重定向自身的方法
        self.data_received = protocol.data_received
        self.eof_received = protocol.eof_received
        self.connection_lost = protocol.connection_lost

        # 通知 real protocol 连接建立
        protocol.connection_made(self.transport)

        # 数据移交给真正的协议对象
        protocol.data_received(self._protocol_detect_buffer)

        self._real_protocol = protocol

        # 清理无用数据和引用
        del self._protocol_factories
        del self._default_protocol_factory
        del self._protocol_detect_buffer
        del self.transport

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

        buffer = self._protocol_detect_buffer + data
        self._protocol_detect_buffer = buffer

        # 协议检测
        for item in self._protocol_factories[:]:
            factory, detector = item

            result = detector(buffer)
            if result == YES:
                logger.debug('协议检测成功: %s 采用 %s 协议', self.peername, factory.__name__)
                self.set_real_protocol(factory())
                return
            elif result == NO:
                self._protocol_factories.remove(item)

        # 检查是否有缺省协议
        if not self._protocol_factories:
            if self._default_protocol_factory:
                factory = self._default_protocol_factory
                logger.info('%s 采用缺省协议: %s', self.peername, factory.__name__)
                self.set_real_protocol(factory())
            else:
                logger.info('不可识别的协议, 断开连接 %s: %r', self.peername, buffer)
                self.transport.close()


def _feature_detector(data, features):
    '''特征串检测函数

    :param data: 数据
    :param features: 特征串
    '''
    unsure = False

    if isinstance(features, bytes):
        features = [features]

    for feature in features:
        if data.startswith(feature):
            return YES
        if feature.startswith(data):
            # 如果 feature 以 data 开头，说明数据不够，不足以判别
            unsure = True

    return UNSURE if unsure else NO


class DummyProtocolFactory:
    def __init__(self, dummy_protocol_class=DummyProtocol):
        self.dummy_protocol_class = dummy_protocol_class

        self._protocol_factories = []
        self._default_protocol_factory = None

    def register_protocol_factory(self, protocol_factory, *, detector=None, features=None, default=None):
        '''注册协议，同时指定检测函数或特征串

        - 检测函数: detector(data), 缺省为 protocol_factory.detector
        - 特征串: bytes 或 [bytes, ...]，缺省为 protocol_factory.features
        - 缺省协议: 其他协议检测完毕，则不做进一步检测，直接采用该协议 

        :param protocol_factory: 要注册的协议
        :param detector: 检测函数
        :param features: 特征串
        :param default: 是否缺省协议
        '''
        assert not (detector and features)

        if not detector and not features:
            detector = getattr(protocol_factory, 'detector', None)
            if not detector:
                features = getattr(protocol_factory, 'features', None)

        if features:
            assert not detector
            detector = functools.partial(_feature_detector, features=features)

        if default is None:
            default = getattr(protocol_factory, 'default', False)

        if default:
            assert not self._default_protocol_factory
            self._default_protocol_factory = protocol_factory
        else:
            assert protocol_factory not in self._protocol_factories
            self._protocol_factories.append((protocol_factory, detector))

    def __call__(self):
        return self.dummy_protocol_class(self)


if __name__ == '__main__':
    import logging

    class BaseProtocol(asyncio.Protocol):
        def connection_made(self, transport):
            logging.info('%s, connection_made', self.__class__.__name__)

        def connection_lost(self, exc):
            logging.info('%s connection_lost: %s', self.__class__.__name__, exc)

        def data_received(self, data):
            logging.info('%s data_received: %s', self.__class__.__name__, data)

    class A(BaseProtocol):
        features = b'A'

    class B(BaseProtocol):
        features = [b'B', b'b']

    class C(BaseProtocol):
        pass

    def C_detector(data):
        if data.startswith(b'C'):
            return YES
        return NO

    class D(BaseProtocol):
        pass

    class XX(BaseProtocol):
        @staticmethod
        def detector(data):
            if len(data) < 2:
                return UNSURE
            if data[0] == data[1]:
                return YES
            return NO

    logging.basicConfig(level='DEBUG')

    factory = DummyProtocolFactory()
    factory.register_protocol_factory(A)
    factory.register_protocol_factory(B)
    factory.register_protocol_factory(C, detector=C_detector)
    factory.register_protocol_factory(D, default=True)
    factory.register_protocol_factory(XX)

    loop = asyncio.get_event_loop()
    host, port = '0.0.0.0', 9999
    loop.run_until_complete(loop.create_server(factory, host, port))
    logger.info('监听: %s:%d', host, port)
    loop.run_forever()
