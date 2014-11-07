# -*- coding: utf-8 -*-
import asyncio


@asyncio.coroutine
def file_get_contents(filename, loop=None):
    '''读取文件内容，支持本地文件和 http 链接

    这里只提供最简单接口，如果需要更复杂的控制，请直接调用相应函数
    '''
    if filename.startswith('http://'):
        import aiohttp      # 避免不必要的依赖

        if not loop:
            loop = asyncio.get_event_loop()

        response = yield from aiohttp.request('GET', filename)
        content = yield from response.read()
        if response.status != 200:
            raise RuntimeError('读取文件内容失败: %d, %s, %r' % (
                response.status, filename, content))
        return content
    else:
        with open(filename, 'rb') as f:
            return f.read()
