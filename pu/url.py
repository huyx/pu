# -*- coding: utf-8 -*-
from urllib import parse


def parse_url(url, default_host=None, parse_params=False):
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

    netloc = Netloc(netloc, default_host).netloc

    if no_scheme:
        scheme = ''

    return parse.ParseResult(scheme, netloc, path, params, query, fragment)


def parse_hostport(hostport, default_host=None):
    return Netloc(hostport, default_host).hostinfo


class Netloc(parse._NetlocResultMixinStr):
    def __init__(self, netloc, default_host=None):
        self.netloc = netloc

        # 处理 hostname:port 不完整的情况
        if self.port is None and default_host:
            self.netloc = '{}:{}'.format(default_host, netloc)

    def __str__(self):
        return self.netloc

    @property
    def hostinfo(self):
        return self.hostname, self.port

    @property
    def userinfo(self):
        return self.username, self.password


class URL(parse._NetlocResultMixinStr):
    def __init__(self, url, default_host=None):
        self.url = url
        self.default_host = default_host

        self.parse()

    def parse(self):
        result = parse_url(self.url, self.default_host)

        self.netloc = result.netloc

        return result

    def __str__(self):
        return self.url


class MySQL(URL):
    db = None
    charset = 'utf8'

    def parse(self):
        result = URL.parse(self)

        for name, value in parse.parse_qsl(result.query):
            if name == 'charset':
                self.charset = value
            else:
                raise Warning('未知参数: {}={}'.format(name, value))

        if result.path:
            self.db = result.path.lstrip('/')
