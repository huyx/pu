# -*- coding: utf-8 -*-

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


if __name__ == '__main__':
    import doctest
    doctest.testmod()
