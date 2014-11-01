Python Utilities
================

Python 编程工具集，本着实用、简单的原则，尽量减少对其他模块的依赖。

由于内容比较杂，所以并不过分追求兼容性。

pu.aio
------

asyncio 相关扩展和工具。

pu.aio.util

- file_get_contents: 读取文件内容或下载 http 页面内容

pu.aio.timer
~~~~~~~~~~~~

提供一个简单的 Timer。

- class Timer

pu.aio.client
~~~~~~~~~~~~~

简单的 Client 类和支持重连的 ReconnectingClient

- class Client
- class ReconnectingClient

pu.aio.dummyprotocol
~~~~~~~~~~~~~~~~~~~~~~

支持动态协议识别，根据收到的数据判断连接实际采用的协议。

- class DummyProtocolFactory
- class DummyProtocol

pu.aio.virtualprotocol
~~~~~~~~~~~~~~~~~~~~~~

!! 请使用 dummyprotocol

支持动态协议识别，根据收到的数据判断连接实际采用的协议，动态协议需要继承自 RealProtocol。

- class VirtualProtocolFactory
- class VirtualProtocol
- class RealProtocol

pu.util
----

- shorten

pu.dictutil
--------

- repr_dict
- Dot
- DotDict
- OrderedDict
- DotOrderedDict

pu.manager
-------

- class Manager: 对象管理器


用法::

    manager = Manager()

    manager.register(1, 'ONE')

    @manager.register
    def a(): pass

    @manager.named('funcb', 'FUNCB')
    def b(): pass

    @manager.register
    class A: pass

    @manager.named('clsb', 'CLSB')
    class B: pass
