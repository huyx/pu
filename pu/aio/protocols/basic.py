# -*- coding: utf-8 -*-
import asyncio


class _PauseableMixin:
    _paused = False

    def pause_reading(self):
        '''暂停读取和处理已经读取的数据
        '''
        self._paused = True
        self.transport.pause_reading()

    def resume_reading(self):
        '''恢复处理
        '''
        self._paused = False
        self.transport.resume_reading()
        self.data_received(b'')


class LineReceiver(asyncio.Protocol, _PauseableMixin):
    '''每次接收一行，支持自动探测行结束符，支持暂停处理

    由于有些数据已经接收到缓冲区内，因此需要 _paused 标志协助处理
    '''
    _buffer = b''
    _delimiter = None

    def _guess_delimiter(self):
        if b'\r\n' in self._buffer:
            self._delimiter = b'\r\n'
        elif b'\n' in self._buffer:
            self._delimiter = b'\n'
        elif b'\r' in self._buffer:
            self._delimiter = b'\r'

    def connection_made(self, transport):
        self.transport = transport

    def write_line(self, line):
        delimiter = self._delimiter or b'\r\n'
        data = line + delimiter
        self.transport.write(data)

    def data_received(self, data):
        self._buffer += data

        if not self._delimiter:
            self._guess_delimiter()
            if not self._delimiter:
                return

        while self._buffer and not self._paused:
            try:
                line, self._buffer = self._buffer.split(self._delimiter, 1)
            except:
                break
            self.line_received(line)

    def line_received(self, line):
        raise NotImplementedError


class IntNStringReceiver(asyncio.Protocol, _PauseableMixin):
    _buffer = b''
    _prefix_length = 0

    def connection_made(self, transport):
        self.transport = transport

    def write_string(self, string):
        strlen = len(string)
        prefix = strlen.to_bytes(self._prefix_length, 'big')
        self.transport.write(prefix + string)

    def data_received(self, data):
        data = self._buffer + data
        prefix_length = self._prefix_length

        while len(data) > prefix_length and not self._paused:
            strlen = int.from_bytes(data[:prefix_length], 'big')
            if len(data) <prefix_length + strlen:
                break
            endpos = prefix_length + strlen
            string, data = data[prefix_length:endpos], data[endpos:]
            self.string_received(string)

        self._buffer = data

    def string_received(self, string):
        raise NotImplementedError


class Int8StringReceiver(IntNStringReceiver):
    _prefix_length = 1


class Int16StringReceiver(IntNStringReceiver):
    _prefix_length = 2


class Int32StringReceiver(IntNStringReceiver):
    _prefix_length = 4
