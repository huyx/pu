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
~~~~~~~~~~~~~~~~~~~~

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

pu.aio.protocols.basic
~~~~~~~~~~~~~~~~~~~~~~

class LineReceiver 类似于 twisted.protocols.basic.LineOnlyReceiver，但支持自动检测行分隔符。

pu.util
-------

- shorten
- get_field(o, field_name)
- set_field(o, field_name, value)
- import_file
- load_any
- reload_any

pu.dictutil
-----------

- repr_dict
- Dot
- DotDict
- OrderedDict
- DotOrderedDict

pu.url
------

- parse_url: 提供更灵活地 url 分析
- parse_hostport
- Netloc

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

    assert manager.get(1) == 'ONE'

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

pu.rcp
------

简单的远程调用协议，文档直接看源代码里面的注释。

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

pu.minimist
-----------

分析命令行参数，源自 `minimist <https://github.com/substack/minimist>`_，目的是
提供一个简单，有一定通用性的命令行参数分析工具。


只提供一个函数接口::

    parse(args, *, lists=[], bools=[], strings=[], defaults={})

示例::

    # 综合示例
    $ python -m pu.minimist -x 3 -y 4 -n5 -abc --beep=boop foo bar baz
    Namespace(_=['foo', 'bar', 'baz'], a=True, b=True, beep='boop', c=True, n=5, x=3, y=4)
  
    $ python -m pu.minimist -a=a -b=b
    Namespace(_=[], a='a', b='b')

    # 参数数组
    $ python -m pu.minimist -a a -a b
    Namespace(_=[], a=['a', 'b'])
  
    # '--' 后面的参数全部保存到 '--'
    $ python -m pu.minimist a -- -b -c d
    Namespace(--=['-b', '-c', 'd'], _=['a'])

    # '-' 后面多个选项，则全部为 bool 类型
    $ python -m pu.minimist -a -b -cd
    Namespace(_=[], a=True, b=True, c=True, d=True)

    # 用 '.' 结尾表示 bool 类型
    $ python -m pu.minimist --arg. x -a. y
    Namespace(_=['x', 'y'], a=True, arg=True)

pu.pattern
----------

设计模式收集

- pu.pattern.observer -- 观察者模式，根据 Python 的特点，只提供了 Observerable，可以注册函数或方法观察者。

