# -*- coding: utf-8 -*-

"""
パケットを投げるスレッドの基底クラス
"""

import socket
import threading
import ipaddress

from model import HachiUtil


class SendThread(threading.Thread):
    def __init__(self, params, sendObj, srcport):
        super(SendThread, self).__init__()
        self.unlimited = params.unlimited.get()
        self.freq = 1 / int(params.pps.get())
        self.data = HachiUtil.ramdom_binary(int(params.datalen.get()))
        self.dstaddr_list = params.dstaddr.address_list()
        self.srcaddr_list = params.srcaddr.address_list()
        self.ip_version = ipaddress.ip_address(self.dstaddr_list[0][0]).version

        # srcportはIntVar()を渡す
        self.srcport = srcport

        self.sendObj = sendObj
        self.stop_flg = False

        # IPv4とIPv6でソケットファミリー分かれる
        if self.ip_version == 4:
            self.family = socket.AF_INET
            self.ZERO_IP = '0.0.0.0'
        else:  # ip_version == 6
            self.family = socket.AF_INET6
            self.ZERO_IP = '::0'

    def run(self):
        # 下位クラスで定義
        pass

    def stop(self):
        self.stop_flg = True
