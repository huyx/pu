# -*- coding: utf-8 -*-
from collections import Mapping
from distutils.version import StrictVersion, LooseVersion
import importlib
import inspect
import re
import sys
import time


def shorten(s, width=80):
    '''
    >>> shorten('a very very very very long sentence', 20)
    'a very very ..(23)..'
    '''
    if not isinstance(s, str):
        s = str(s)

    length = len(s)
    if length < width:
        return s

    cut_length = length - width + 6
    x = len(str(cut_length))
    cut_length += x

    # 长度调整
    if x != len(str(cut_length)):
        cut_length += 1

    end_pos = length - cut_length
    return s[:end_pos] + '..(%d)..' % cut_length


def bytes_fromhex(s):
    return bytes.fromhex(re.sub('\s', '', s))


def iterattrs(ob, protect_member=False):
    '''返回对象的属性列表
    '''
    if protect_member:
        names = (n for n in sorted(dir(ob)) if not n.startswith('__'))
    else:
        names = (n for n in sorted(dir(ob)) if not n.startswith('_'))

    return iter((n, getattr(ob, n)) for n in names)


def deep_encode(ob, encoding='utf_8', errors='strict'):
    '''深入数据结构内部，尽可能把字符串编码
    '''
    if isinstance(ob, bytes):
        return ob
    elif isinstance(ob, str):
        return ob.encode(encoding, errors)
    elif isinstance(ob, tuple):
        return tuple(deep_encode(x, encoding, errors) for x in ob)
    elif isinstance(ob, list):
        return [deep_encode(x, encoding, errors) for x in ob]
    elif isinstance(ob, Mapping):
        new = ob.__class__()
        for key, value in ob.items():
            key = deep_encode(key, encoding, errors)
            value = deep_encode(value, encoding, errors)
            new[key] = value
        return new
    else:
        return ob


def deep_decode(ob, encoding='utf_8', errors='strict'):
    '''深入数据结构内部，尽可能把 bytes 解码
    '''
    if isinstance(ob, bytes):
        return ob.decode(encoding, errors)
    elif isinstance(ob, str):
        return ob
    elif isinstance(ob, tuple):
        return tuple(deep_decode(x, encoding, errors) for x in ob)
    elif isinstance(ob, list):
        return [deep_decode(x, encoding, errors) for x in ob]
    elif isinstance(ob, Mapping):
        new = ob.__class__()
        for key, value in ob.items():
            key = deep_decode(key, encoding, errors)
            value = deep_decode(value, encoding, errors)
            new[key] = value
        return new
    else:
        return ob


def format_args(args, kwargs):
    items = list(map(repr, args))
    if isinstance(kwargs, dict):
        kwargs = sorted(kwargs.items())
    items.extend(map(lambda kv: '%s=%r' % kv, kwargs))
    return ', '.join(items)


def format_time(t=None, fmt='%Y-%m-%d %H:%M:%S'):
    return time.strftime(fmt, time.localtime(t))


def get_field(o, field_name):
    '''支持多级对象的读取

    语法: .attr:index#index ...

    - .attr
    - :index     [index]
    - #index     [int(index)]
    '''
    # 开头的 . 可以省略
    if field_name[0] not in '.:#':
        field_name = '.' + field_name

    names = re.findall(r'[.:#]\w+', field_name)
    for name in names:
        flag = name[0]
        name = name[1:]
        if flag == '.':
            o = getattr(o, name)
        elif flag == ':':
            o = o[name]
        else:
            o = o[int(name)]

    return o


def set_field(o, field_name, value):
    '''多级对象属性的修改
    '''
    # 开头的 . 可以省略
    if field_name[0] not in '.:#':
        field_name = '.' + field_name

    * names, last_name = re.findall(r'[.:#]\w+', field_name)
    for name in names:
        flag = name[0]
        name = name[1:]
        if flag == '.':
            o = getattr(o, name)
        elif flag == ':':
            o = o[name]
        else:
            o = o[int(name)]

    flag, name = last_name[0], last_name[1:]
    if flag == '.':
        setattr(o, name, value)
    elif flag == ':':
        o[name] = value
    else:
        o[int(name)] = value


def to_bool(value):
    if isinstance(value, bool):
        return value
    elif isinstance(value, str):
        orig_value = value
        value = orig_value.strip().lower()

        if value in ['y', 'yes', 't', 'true', '1']:
            return True
        elif value in ['n', 'no', 'f', 'false', '0']:
            return False
        else:
            raise ValueError('%r 不能转换成布尔类型' % orig_value)
    else:
        return bool(value)


def to_hex(value: bytes, delimiter=' ', lower=True):
    fmt = '%02x' if lower else '%02X'
    return delimiter.join(fmt % b for b in value)


def dump_data(data: bytes, maxlength=80):
    dlen = len(data)
    data = data[:maxlength]
    return '({}) {} - {}'.format(dlen, to_hex(data), data)


def import_file(module_name, filepath):
    import importlib.machinery

    loader = importlib.machinery.SourceFileLoader(module_name, filepath)
    return loader.load_module()


def load_any(name):
    '''根据对象名称加载对象
    '''
    try:
        return importlib.import_module(name)
    except ImportError:
        module_name, name = name.rsplit('.', 1)
        module = importlib.import_module(module_name)
        return getattr(module, name)


def _reload_module_by_name(module_name):
    module = sys.modules.get(module_name)

    if module:
        module = importlib.reload(module)
    else:
        module = importlib.import_module(module_name)

    return module


def reload_any(ob):
    '''reload 任何对象

    例如::

        reload_any(os.path)    # 直接重新加载对象
        reload_any('sys.path') # 根据名称加载对象

    :param ob: 对象(适合于有 __name__ 的对象)或对象名称
    '''
    # 对于模块，直接加载
    if inspect.ismodule(ob):
        return importlib.reload(ob)

    if isinstance(ob, str):
        name = ob

        # 作为模块名尝试一下
        try:
            return _reload_module_by_name(name)
        except ImportError:
            pass

        # 一定是 "模块.对象" 的形式
        assert '.' in name
        module_name, ob_name = ob.rsplit('.', 1)
    else:
        module_name = ob.__module__
        ob_name = ob.__name__

    module = _reload_module_by_name(module_name)

    return getattr(module, ob_name)


def make_key(args, kwargs, kwargs_mark=object()):
    '''根据函数参数 args, kwargs 创建键值

    特点: 生成一个没有嵌套（args 和 kwargs 的值中没有 tuple 值）的 tuple
    限制: args 和 kwargs 的值必须 hashable

    :param args: tuple
    :param kwargs: dict
    :param kwargs_mark: 在有 kwargs 非空的情况下，用来分割 args 和 kwargs
    '''
    key = args

    if kwargs:
        key += kwargs_mark
        for item in sorted(kwargs.items):
            key += item

    return key


def default(value, exceptions=Exception):
    '''函数出现异常时返回缺省值

    用法1:

    default_int = default(0)(int)

    用法2:

    @default(0)
    def my_int(value):
        return int(value)

    用法3:

    @default('-type error-', TypeError)
    @default('-value error-', ValueError)
    def my_int(value):
        return int(value)

    示例:

    >>> default('错了')(int)(None)
    '错了'
    >>> default('类型错误', TypeError)(int)(None)
    '类型错误'
    >>> default('类型或值错误', (TypeError, ValueError))(int)('not a integer')
    '类型或值错误'
    '''
    def outer(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exceptions:
                return value
        return inner
    return outer


def _cmp(a, b):
    return (a > b) - (a < b)

def compare_versions(version1, version2):
    try:
        return _cmp(StrictVersion(version1), StrictVersion(version2))
    # in case of abnormal version number, fall back to LooseVersion
    except ValueError:
        pass
    try:
        return _cmp(LooseVersion(version1), LooseVersion(version2))
    except TypeError:
    # certain LooseVersion comparions raise due to unorderable types,
    # fallback to string comparison
        return _cmp([str(v) for v in LooseVersion(version1).version],
                   [str(v) for v in LooseVersion(version2).version])


def format_size(size):
    if size > 1000 * 1000:
        return '%.1fMB' % (size / 1000.0 / 1000)
    elif size > 10 * 1000:
        return '%ikB' % (size / 1000)
    elif size > 1000:
        return '%.1fkB' % (size / 1000.0)
    else:
        return '%ibytes' % size


if __name__ == '__main__':
    import doctest
    doctest.testmod()
