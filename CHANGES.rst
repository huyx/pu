0.7.1(2014-11-14)
-----------------

- 整理: 移动 test 目录

0.7.0(2014-11-14)
-----------------

- 添加 pu.rcp -- 一个简单远程调用协议(Remote Call Protocol)

0.6.7(2014-11-12)
-----------------

- BUGFIX: pu.dictutil.DotOrderedDict 继承类中自定义 __repr__ 引起错误（因为内部异常处理中引用了 %r）

0.6.6(2014-11-12)
-----------------

- pu.util.deep_encode -- 深入数据结构内部，尽可能把字符串编码
- pu.util.deep_decode -- 深入数据结构内部，尽可能把 bytes 解码

0.6.5(2014-11-12)
-----------------

- iterattrs -- 增加参数，控制是否返回保护属性

0.6.4(2014-11-12)
-----------------

- pu.util.iterattrs -- 返回指定对象的属性列表

0.6.3(2014-11-07)
-----------------

- BUGFIX: pu.pcap IP 包构造错误

0.6.2(2014-11-07)
-----------------

- 读取 http 文件出现错误时抛出异常


0.6.1(2014-11-07)
-----------------

- BUGFIX: pu.pcap TCP flags 分析错误
- 添加 pu.simplefilter -- 简单过滤器
- 添加 example\pcap.py

0.6.0(2014-11-06)
-----------------

- 添加 class pu.datatype.pretty_bytes
- pu.pcap: 网络抓包工具

0.5.5(2014-11-01)
-----------------

- pu.util.bytes_fromhex: 允许比 bytes.fromhex 更宽松的输入

0.5.4(2014-11-01)
-----------------

- BUGFIX: pu.aio.timer.Timer 添加类成员 __timer

0.5.3(2014-11-01)
-----------------

- 添加 pu.aio.util.file_get_contents


0.5.2(2014-10-31)
-----------------

- dictutil: Dot 增加 __contains__

0.5.1(2014-10-31)
-----------------

- dictutil: 改进 Dot 的 __repr__ 和 __str__

0.5.0(2014-10-31)
-----------------

- 增加 dummyprotocol, 取代 virtualprotocol

0.4.4(2014-10-30)
-----------------

- aio 中各个模块采用自己的 logger

0.4.3(2014-10-30)
-----------------

- dictutil.Dot: 添加 get 和 setdefault 方法

0.4.3(2014-10-30)
-----------------

- client.Client: 修改 connect 方法为 coroutine
- 版本: Alpha 改为 Beta

0.4.2(2014-10-29)
-----------------

- 允许指定 yaml 文件编码（缺省为 utf-8）

0.4.1(2014-10-29)
-----------------

- virtualprotocol: 允许指定缺省协议，去除原来一个应用只能使用一个虚拟协议的限制

0.4.0(2014-10-28)
-----------------

- 添加 manager 模块

0.3.2(2014-10-27)
-----------------

- BUGFIX: dictutil.Dot 应该支持 [key] 方式访问

0.3.1(2014-10-27)
-----------------

- 完善软件包版本信息

0.3.0(2014-10-26)
-----------------

- dictutil -- repr_dict, Dot, DotDict, OrderedDict, DotOrderedDict

0.2.0(2014-10-25)
-----------------

- yamlfile -- add !include tag

0.1.1(2014-10-25)
-----------------

- Add MANIFEST.in

0.1.0(2014-10-25)
-----------------

- pu.aio.client
- pu.aio.timer
- pu.aio.virtualprotocol

- pu.util.shorten
