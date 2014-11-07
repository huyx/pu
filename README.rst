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
-----------

- repr_dict
- Dot
- DotDict
- OrderedDict
- DotOrderedDict

pu.manager
----------

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

pu.datatype
-----------

自定义数据类型

- class pretty_bytes -- 支持 hex 格式

示例::

    pb = pretty_bytes(b'\xaa\xbb')
    assert '{0:hex}'.format(pb) == 'aabb'

pu.pcap
-------

网络抓包工具，参考:

- http://www.binarytides.com/python-packet-sniffer-code-linux/

命令行用法::

    python -m pu.pcap				# Windows/Linux
    python -m pu.pcap eth1			# Linux
    python -m pu.pcap lo			# Linux
    python -m pu.pcap 192.168.0.100	# Windows

程序中的用法::

    from pu.pcap import pcap

    for packet in pcap('eth1'):
         print(packet)

pu.simplefilter
---------------

简单的过滤器，支持的语法::

    <filter1> && <filter2> || <filter3> && <filter4> ...

每个 filter 的格式::

    <name><op><pattern>

其中 op:

- = -- 存在且相等
- != -- 不存在或不等于
- ~= -- 匹配(支持 * ?)
- !~= -- 不匹配(支持 * ?)

如果 op 加一个前缀 `#`, 表示 pattern 以 hex 字符串格式指定。

示例::

    sip = 192.168.0.1 && dport = 80 || dport = 8080

