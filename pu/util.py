# -*- coding: utf-8 -*-
from collections import Mapping
import re
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


if __name__ == '__main__':
    import doctest
    doctest.testmod()
