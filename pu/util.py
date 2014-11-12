# -*- coding: utf-8 -*-
import re


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


def iterattrs(ob):
    '''返回对象的属性列表
    '''
    names = sorted(dir(ob))
    return iter((n, getattr(ob, n)) for n in names if not n.startswith('__'))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
