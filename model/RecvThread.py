# -*- coding: utf-8 -*-

import socket
import threading
import ipaddress

from controller import RxController


class RecvThread(threading.Thread):
    """ パケットを受け取るスレッドの基底クラス """

    def __init__(self, params, shareObj):
        super(RecvThread, self).__init__()
        self.shareObj = shareObj
        self.shareObj.count = 0
        self.shareObj.total = 0
        self.ip = params.ip.get()
        self.port = int(params.port.get())
        self.stop_flg = False
        self.recv_buf = RxController.MAX_DATALEN
        self.address = (self.ip, self.port)

        # IPv4とIPv6でソケットファミリー分かれる
        self.family = socket.AF_INET if ipaddress.ip_address(
            self.ip).version == 4 else socket.AF_INET6

    def run(self):
        # 下位クラスで定義
        pass

    def stop(self):
        self.stop_flg = True
