# -*- coding: utf-8 -*-
from urllib import parse


def urlparse(url, *, default_host=None, parse_params=False):
    '''更灵活的 url 分析

    url 格式:

        <scheme>://<netloc>/<path>;<params>?<query>#<fragment>

    netloc 格式(未指定 default_host 时):

        [<username>[:<password>]]@<hostname>[:<port>]

    netloc 格式(指定了 default_host 时):

        [<username>[:<password>]]@[<hostname>:]<port>

    :param parse_params: 对于未知协议，指定是否分析 params 字段
    '''
    no_scheme = '://' not in url

    if no_scheme:
        if parse_params:
            scheme_na = parse.uses_params[0]
        else:
            scheme_na = 'unknown'

        url = scheme_na + '://' + url

    result = parse.urlparse(url)
    scheme, netloc, path, params, query, fragment = result

    # 处理 hostname:port 不完整的情况
    if result.port is None and default_host:
        netloc = '{}:{}'.format(default_host, netloc)

    if no_scheme:
        scheme = ''

    return parse.ParseResult(scheme, netloc, path, params, query, fragment)
