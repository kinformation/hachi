# -*- coding: utf-8 -*-

import socket
from contextlib import closing

from model import RecvThread


class RecvTcpThread(RecvThread.RecvThread):
    """ TCPパケットを受け取るスレッド """

    def __init__(self, params, shareObj):
        super().__init__(params, shareObj)

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
            self.shareObj.count += 1
            self.shareObj.total += len(rcvmsg)
