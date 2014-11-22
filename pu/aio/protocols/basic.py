# -*- coding: utf-8 -*-
import asyncio


class LineReceiver(asyncio.Protocol):
    '''每次接收一行，支持自动探测行结束符，支持暂停处理

    由于有些数据已经接收到缓冲区内，因此需要 _paused 标志协助处理
    '''
    _buffer = b''
    _delimiter = None
    _paused = False

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
        data = line + self._delimiter or b'\r\n'
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

    def line_received(self, line):
        raise NotImplementedError
