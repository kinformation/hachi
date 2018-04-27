# -*- coding: utf-8 -*-

"""
UDPパケットを受け取るスレッド
"""

import socket
from contextlib import closing

from model import RecvThread


class RecvUdpThread(RecvThread.RecvThread):
    def __init__(self, host, port, share_obj):
        super().__init__(host, port, share_obj)

        self.sock = socket.socket(self.family, socket.SOCK_DGRAM)
        self.sock.bind(self.address)
        # ノンブロッキング受信(recvfrom()受信を待たない)
        self.sock.setblocking(False)

    def run(self):
        with closing(self.sock):
            self._receive()

    def _receive(self):
        while not self.stop_flg:
            try:
                data = self.sock.recvfrom(self.recv_buf)
            except socket.error:
                pass
            else:
                self.share_obj.count += 1
                self.share_obj.total += len(data[0])
