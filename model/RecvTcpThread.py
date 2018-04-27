# -*- coding: utf-8 -*-

"""
TCPパケットを受け取るスレッド
"""

import socket
from contextlib import closing

from model import RecvThread


class RecvTcpThread(RecvThread.RecvThread):
    def __init__(self, host, port, share_obj):
        super().__init__(host, port, share_obj)

        self.sock = socket.socket(self.family, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(self.address)
        self.sock.listen()

    def run(self):
        with closing(self.sock):
            self._receive()

    def _receive(self):
        clientsock, _ = self.sock.accept()
        while not self.stop_flg:
            rcvmsg = clientsock.recv(self.recv_buf)
            if len(rcvmsg) <= 0:
                clientsock, _ = self.sock.accept()
                pass
            self.share_obj.count += 1
            self.share_obj.total += len(rcvmsg)


if __name__ == '__main__':
    host = '169.254.1.80'
    port = '12000'
    share_obj = 0
    thread = RecvTcpThread(host, port, share_obj)
    thread.start()
