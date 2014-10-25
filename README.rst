Python Utilities
================

Python 编程工具集，本着实用、简单的原则，尽量减少对其他模块的依赖。

由于内容比较杂，所以并不过分追求兼容性。

pu.aio
------

asyncio 相关扩展和工具。

pu.aio.timer
------------

提供一个简单的 Timer。

- class Timer

pu.aio.client
-------------

简单的 Client 类和支持重连的 ReconnectingClient

- class Client
- class ReconnectingClient

pu.aio.virtualprotocol
----------------------

支持动态协议识别，根据收到的数据判断连接实际采用的协议。

- class VirtualProtocol
- class RealProtocol
