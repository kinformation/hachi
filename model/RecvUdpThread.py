# -*- coding: utf-8 -*-

import socket
from contextlib import closing

from model import RecvThread


class RecvUdpThread(RecvThread.RecvThread):
    """ UDPパケットを受け取るスレッド """

    def __init__(self, params, shareObj):
        super().__init__(params, shareObj)

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
                self.shareObj.count += 1
                self.shareObj.total += len(data[0])
