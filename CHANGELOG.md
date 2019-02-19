V0.20.0(2019-02-19)

- README, CHANGELOG 采用 Markdown 格式

V0.19.8(2019-02-19)

- 兼容性：asyncio.async -> asyncio.Task

V0.19.0(2015-4-7)

- 增加 pu.aiotimer: asyncio 定时器、定时器管理器

V0.18.0(2015-3-18)

- 增加 pu.util.default: 指定产生异常时的缺省值

V0.17.3(2015-3-17)

- dictutil 增加 LastUpdatedOrderedDict

V0.17.2(2015-3-3)

- pubsub 改善调试信息输出

V0.17.1(2015-3-2)

- 增加 pu.util.dump_data

V0.17.0(2015-2-28)

- 增加 pu.autopdb: 遇到未处理异常时自动进入调试状态

V0.16.1(2015-2-28)

- BUGFIX: pu.aio.client.ReconnectingClient 修正连接反复断开后引起连接数增多的问题

V0.16.0(2015-2-26)

- distance: 计算地球表面之间两点的距离

V0.15.2(2015-2-6)

- pubsub: 改善信息输出格式

V0.15.1(2015-2-6)

- BUGFIX: pubsub 中 psubscribe 时产生异常

V0.15.0(2015-2-6)

- pubsub: 支持指定优先级的发布/订阅模式的实现

V0.14.4(2015-2-3)

- dictutil.Dict: 允许指定显示时字段的顺序，大道至简，推荐使用

0.14.3(2015-1-31)

- lazydict: 改善错误信息

0.14.2(2015-1-31)

- BUGFIX: lazydict 中 smart_set 处理字典时出错

0.14.1(2015-1-31)

- lazydict: 增加 smart_get, smart_set，支持形如 'item.100.attrname' 的 key

0.14.0(2015-1-30)

- 增加 lazydict: 重载 setdefault，可以在 key 不存在时才计算 default 值（通过 factory 参数）

0.13.2(2015-1-29)

- BUGFIX: util.reload_any 变量名引用错误

0.13.1(2015-1-29)

- BUGFIX: util.reload_any 处理名称中没有 . 情况

0.13.0(2015-1-29)

- event.py: 增加基于 list 的事件处理机制
- 增加简单的 cache 类
- 增加 util.make_key: 根据函数参数 args, kwargs 创建键值

0.12.2(2015-1-20)

- 添加 pu.misc.aiohttp.reloadable_handler 支持 web handler 的自动重新加载

0.12.1(2015-1-7)

- BUGFIX: 修正用 reload_all 首次加载对象时导致的异常

0.12.0(2015-1-7)

- 增加 load_any 和 reload_any 实现任意对象的加载和重新加载

0.11.5(2014-12-17)

- pu.util 增加: import_file
- 增加 url 模块: 用于分析各种 url

0.11.2(2014-12-10)

- pu.util 增加: parse_hostport

0.11.1(2014-12-9)

- 修正拼写错误: Observerable ==> Observable
- pu.util 增加: to_bool，to_hex

0.11.0(2014-11-29)

- 添加设计模式: 观察者模式
- BUGFIX: 修正运算符优先级错误

0.10.10(2014-11-26)

- 增加 Int8StringReceiver, Int16StringReceiver, Int32StringReceiver

0.10.9(2014-11-22)

- LineReceiver 添加 pause_reading, resume_reading 支持暂停数据处理

0.10.8(2014-11-22)

- pu.minimist.parse: 增加 comments 参数，控制是否允许 # 注释
- pu.aio.protocols.cli: 不再支持行内注释，仅支持整行注释

0.10.7(2014-11-22)

- 增加 get_field, set_field: 支持多级对象的操作

0.10.6(2014-11-21)

- 重构: 规范 Cli 接口消息格式

0.10.5(2014-11-21)

- 整理 version 和 logger 的定义

0.10.4(2014-11-20)

- 修改 setup.py，兼容 Python2.x

0.10.3(2014-11-20)

- pu.util: 增加 format_time 函数

0.10.2(2014-11-20)

- pu.aio.protocols.cli: 完善异常处理

0.10.1(2014-11-20)

- pu.minimist: 修改分析结果为 dict 类型
- pu.util: 增加 format_args 函数
- pu.aio.protocols.cli: 修改参数分析

0.10.0(2014-11-19)

- 增加 pu.aio.protocols.cli.Cli -- 命令行接口协议

0.9.2(2014-11-17)

- pu.minimist -- 选项以 . 结尾表示 bool 类型

0.9.1(2014-11-17)

- 整理目录结构
- BUGFIX: 测试代码中相对 import 改为绝对 import

0.9.0(2014-11-17)

- 添加 pu.aio.protocols.LineReceiver -- 基于行的协议

0.8.0(2014-11-17)

- 添加 pu.minimist -- 命令行参数分析工具

0.7.2(2014-11-14)

- 添加 pu.rcp 的说明

0.7.1(2014-11-14)

- 整理: 移动 test 目录

0.7.0(2014-11-14)

- 添加 pu.rcp -- 一个简单远程调用协议(Remote Call Protocol)

0.6.7(2014-11-12)

- BUGFIX: pu.dictutil.DotOrderedDict 继承类中自定义 __repr__ 引起错误（因为内部异常处理中引用了 %r）

0.6.6(2014-11-12)

- pu.util.deep_encode -- 深入数据结构内部，尽可能把字符串编码
- pu.util.deep_decode -- 深入数据结构内部，尽可能把 bytes 解码

0.6.5(2014-11-12)

- iterattrs -- 增加参数，控制是否返回保护属性

0.6.4(2014-11-12)

- pu.util.iterattrs -- 返回指定对象的属性列表

0.6.3(2014-11-07)

- BUGFIX: pu.pcap IP 包构造错误

0.6.2(2014-11-07)

- 读取 http 文件出现错误时抛出异常

0.6.1(2014-11-07)

- BUGFIX: pu.pcap TCP flags 分析错误
- 添加 pu.simplefilter -- 简单过滤器
- 添加 example\pcap.py

0.6.0(2014-11-06)

- 添加 class pu.datatype.pretty_bytes
- pu.pcap: 网络抓包工具

0.5.5(2014-11-01)

- pu.util.bytes_fromhex: 允许比 bytes.fromhex 更宽松的输入

0.5.4(2014-11-01)

- BUGFIX: pu.aio.timer.Timer 添加类成员 __timer

0.5.3(2014-11-01)

- 添加 pu.aio.util.file_get_contents

0.5.2(2014-10-31)

- dictutil: Dot 增加 __contains__

0.5.1(2014-10-31)

- dictutil: 改进 Dot 的 __repr__ 和 __str__

0.5.0(2014-10-31)

- 增加 dummyprotocol, 取代 virtualprotocol

0.4.4(2014-10-30)

- aio 中各个模块采用自己的 logger

0.4.3(2014-10-30)

- dictutil.Dot: 添加 get 和 setdefault 方法

0.4.3(2014-10-30)

- client.Client: 修改 connect 方法为 coroutine
- 版本: Alpha 改为 Beta

0.4.2(2014-10-29)

- 允许指定 yaml 文件编码（缺省为 utf-8）

0.4.1(2014-10-29)

- virtualprotocol: 允许指定缺省协议，去除原来一个应用只能使用一个虚拟协议的限制

0.4.0(2014-10-28)

- 添加 manager 模块

0.3.2(2014-10-27)

- BUGFIX: dictutil.Dot 应该支持 [key] 方式访问

0.3.1(2014-10-27)

- 完善软件包版本信息

0.3.0(2014-10-26)

- dictutil -- repr_dict, Dot, DotDict, OrderedDict, DotOrderedDict

0.2.0(2014-10-25)

- yamlfile -- add !include tag

0.1.1(2014-10-25)

- Add MANIFEST.in

0.1.0(2014-10-25)

- pu.aio.client
- pu.aio.timer
- pu.aio.virtualprotocol
- pu.util.shorten
