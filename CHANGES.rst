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
