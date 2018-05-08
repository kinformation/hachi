# -*- coding: utf-8 -*-

"""
パケットを投げるスレッドの基底クラス
"""

import socket
import threading
import ipaddress

from model import HachiUtil


class SendThread(threading.Thread):
    def __init__(self, params, counter):
        super(SendThread, self).__init__()
        self.unlimited = params.unlimited.get()
        self.freq = 1 / int(params.pps.get())
        self.payload = HachiUtil.ramdom_binary(int(params.datalen.get()))
        self.host = params.host.get()
        self.address = (self.host, int(params.dstport.get()))

        # srcportはIntVar()を渡す
        self.srcport_obj = params.srcport

        self.counter = counter
        self.stop_flg = False

        # IPv4とIPv6でソケットファミリー分かれる
        self.family = socket.AF_INET if ipaddress.ip_address(
            self.host).version == 4 else socket.AF_INET6

    def run(self):
        # 下位クラスで定義
        pass

    def stop(self):
        self.stop_flg = True
