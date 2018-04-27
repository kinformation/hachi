# -*- coding: utf-8 -*-

"""
パケットを受け取るスレッドの基底クラス
"""

import socket
import threading
import ipaddress


class RecvThread(threading.Thread):
    def __init__(self, host, port, share_obj):
        super(RecvThread, self).__init__()
        self.share_obj = share_obj
        self.share_obj.count = 0
        self.share_obj.total = 0
        self.stop_flg = False
        self.recv_buf = 9000
        self.address = (host, int(port))

        # IPv4とIPv6でソケットファミリー分かれる
        self.family = socket.AF_INET if ipaddress.ip_address(
            host).version == 4 else socket.AF_INET6

    def run(self):
        # 下位クラスで定義
        pass

    def stop(self):
        self.stop_flg = True
