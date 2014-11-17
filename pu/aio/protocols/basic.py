# -*- coding: utf-8 -*-
import asyncio


class LineReceiver(asyncio.Protocol):
    _buffer = b''
    _delimiter = None

    def connection_made(self, transport):
        self.transport = transport

    def _guess_delimiter(self):
        if b'\r\n' in self._buffer:
            self._delimiter = b'\r\n'
        elif b'\n' in self._buffer:
            self._delimiter = b'\n'
        elif b'\r' in self._buffer:
            self._delimiter = b'\r'

    def data_received(self, data):
        self._buffer += data

        if not self._delimiter:
            self._guess_delimiter()
            if not self._delimiter:
                return

        lines = self._buffer.split(self._delimiter)
        self._buffer = lines.pop(-1)
        for line in lines:
            self.line_received(line)

    def line_received(self, line):
        raise NotImplementedError

