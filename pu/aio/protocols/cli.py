# -*- coding: utf-8 -*-
import asyncio
import logging
import textwrap

from pu import minimist
from pu.aio.protocols.basic import LineReceiver


logger = logging.getLogger(__name__)


class Error(Exception):
    code = 100
    message = '错误'

    def __init__(self, message=None):
        super().__init__(message)

        if message:
            self.message = message


class DecodeError(Error):
    code = 101
    message = '解码错误'


class CommandNotFound(Error):
    code = 102
    message = '命令不存在'


class BadFormat(Error):
    code = 103
    message = '命令格式错误'


class InvalidParam(Error):
    code = 104
    message = '无效参数'


class Cli(LineReceiver):
    encoding = 'utf_8'

    def __init__(self, password=None):
        self.password = password

    def write_line(self, line):
        if not self.password:
            if isinstance(line, str):
                line = line.encode(self.encoding)
            super().write_line(line)

    def write(self, data):
        if not self.password:
            self.transport.write(data)

    def _write_lines(self, lines, prefix='M'):
        if self.password:
            return
        if isinstance(lines, str):
            lines = [lines]
        self.write_line(prefix + ' ' + lines.pop(0))
        for line in lines:
            self.write_line('  ' + line)

    def write_error(self, message):
        self._write_lines(message, 'E')

    def write_response(self, message):
        self._write_lines(message, '-')

    def write_notify(self, message):
        self._write_lines(message, 'N')

    def splitlines(self, s):
        return s.split(self._delimiter.decode())

    def line_received(self, line):
        try:
            line = line.decode(self.encoding).strip()
        except Exception as e:
            raise DecodeError()

        if not line:
            return

        if line.startswith('#'):
            return

        kwargs = minimist.parse(line, comments=False)

        command, *args = kwargs.pop('_')

        handler_name = command.upper()

        try:
            handler = self.get_handler(handler_name)
        except Error as e:
            self.write_error('%d: %s' % (e.code, e.message))
        else:
            if not self.password or handler.__name__ == 'AUTH':
                try:
                    handler(*args, **kwargs)
                except Error as e:
                    self.write_error('%d: %s' % (e.code, e.message))
                except Exception as e:
                    logger.exception('处理 %s 出错: %s', handler.__name__, e)
                    self.write_error('999: %s' % (e))

    def get_handler(self, handler_name):
        handler = getattr(self, handler_name, None)

        if not handler:
            # 支持命令缩写
            handler_names = [n for n in dir(self) if n.startswith(handler_name)]
            if len(handler_names) != 1:
                raise CommandNotFound()
            handler_name = handler_names[0]
            handler = getattr(self, handler_name)

        return handler

    def AUTH(self, password):
        if self.password == password:
            self.password = None

    def HELP(self, *commands):
        '''查看帮助信息
        '''
        docs = []
        if commands:
            for command in commands:
                handler = getattr(self, command.upper(), None)
                if handler:
                    # 重新格式化文档
                    doc = handler.__doc__ or '-'
                    lines = doc.splitlines()

                    docs.append('%-20s%s' % (command, lines.pop(0)))

                    # 处理后续行的缩进问题
                    lines = textwrap.dedent('\n'.join(lines)).splitlines()

                    for line in lines:
                        docs.append('%-20s%s' % (' ', line))
                else:
                    docs.append('%-20s不存在' % command)
        else:
            commands = [m for m in dir(self) if m.upper() == m]
            for command in commands:
                handler = getattr(self, command.upper(), None)
                doc = handler.__doc__ or '-'
                doc = doc.splitlines()[0]
                doc = '%-20s%s' % (command, doc)
                docs.append(doc)

        self.write_response(docs)

    def set_encoding(self, encoding):
        try:
            assert '测试'.encode(encoding).decode(encoding) == '测试'
        except:
            raise InvalidParam('无效编码类型 %s' % encoding)
        else:
            self.encoding = encoding

    def ENCODING(self, encoding=None):
        '''设置编码
        命令格式: encoding [gbk|utf-8|...]
        '''
        if encoding:
            if self.encoding != encoding:
                self.set_encoding(encoding)
        else:
            self.write_response('encoding: %s' % self.encoding)

    def GBK(self):
        self.ENCODING('gbk')

    def UTF8(self):
        self.ENCODING('utf_8')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(loop.create_server(
        lambda : Cli('aa'), '0.0.0.0', 9999))
    loop.run_forever()
