# -*- coding: utf-8 -*-
from ast import literal_eval
import re
import shlex


def guess(value):
    try:
        return literal_eval(value)
    except:
        pass

    try:
        if value.lower() in ('yes', 'true'):
            return True
        if value.lower() in ('no', 'false'):
            return False
    except:
        pass

    return value


patterns = (
    ('--', re.compile(r'^--$')),  # -- arg1 arg2
    ('--arg=value', re.compile(r'^--(.*)=(.*)$')),
    ('-a=value', re.compile(r'^-(.*)=(.*)$')),
    ('--noarg', re.compile(r'^--no(.*)$')),
    ('--arg.', re.compile(r'^--[^.]*\.$')),  # --arg.
    ('-a.', re.compile(r'^-.\.$')),  # -a.
    ('--arg', re.compile(r'^--[^.]*$')),  # --arg value | --arg
    ('-a', re.compile(r'^-.$')),  # -a value | -a
    ('-aNN', re.compile(r'^-(.)([0-9]+)$')),  # -a88
    ('-abc', re.compile(r'^-(.*)$')),  # -a -b -c
    )


def parse(args, *, lists=[], bools=[], strings=[], defaults={}, comments=True):
    '''分析命令行参数
    '''
    if isinstance(args, str):
        args = shlex.split(args, comments=comments)

    # 准备结果
    result = {}

    result['_'] = []

    # 列表选项处理
    for name in lists:
        result[name] = []

    # 定义设定选项的函数
    def set_arg(name, value, is_string=False):
        if not is_string and isinstance(value, str):
            value = guess(value)

        orig_value = result.get(name, None)

        if orig_value is not None:
            # 多个值自动转换成列表
            if isinstance(orig_value, list):
                orig_value.append(value)
            else:
                result[name] = [orig_value, value]
        else:
            result[name] = value

    while args:
        arg = args.pop(0)

        name = arg.lstrip('-')

        if name in bools:
            set_arg(name, True)
            continue

        if name in strings:
            assert args, '{} must follow a value'.format(arg)
            value = args.pop(0)
            set_arg(name, value, is_string=True)
            continue

        for cond, pattern in patterns:
            m = pattern.match(arg)
            if m:
                if cond == '--':
                    set_arg('--', args)
                    args = []
                    break
                elif cond in ('--arg=value', '-a=value'):
                    set_arg(*m.groups())
                elif cond == '--noarg':
                    set_arg(m.group(1), False)
                elif cond in ('--arg', '-a'):
                    if args:
                        value = args[0]
                        if value[0] != '-':
                            args.pop(0)
                            set_arg(name, value)
                        else:
                            set_arg(name, True)
                    else:
                        set_arg(name, True)
                elif cond in ('--arg.', '-a.'):
                    name = name[:-1]  # 去掉末尾的 .
                    set_arg(name, True)
                elif cond == '-aNN':
                    name, value = m.groups()
                    set_arg(name, int(value))
                elif cond == '-abc':
                    for n in name:
                        set_arg(n, True)
                break
        else:
            set_arg('_', arg)

    # 缺省值处理
    for name, value in defaults.items():
        if name not in result:
            result[name] = value

    return result


if __name__ == '__main__':
    import sys

    print(parse(sys.argv[1:]))
