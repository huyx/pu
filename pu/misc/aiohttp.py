# -*- coding: utf-8 -*-
from aiohttp import web
from pu.util import reload_any, load_any


def reloadable_handler(real_handler, reload=True):
    '''自动重新加载的 handler

    :param real_handler: handler 对象或名称
    :param reload: 是否自动加载
    '''
    def loader(request):
        try:
            if reload:
                handler = reload_any(real_handler)
            else:
                handler = load_any(real_handler)
        except Exception as e:
            return web.Response(text='加载/重新加载 {} 时产生异常: {}'.format(real_handler, e))

        return handler(request)
    return loader
