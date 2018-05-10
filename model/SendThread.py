# -*- coding: utf-8 -*-

"""
パケットを投げるスレッドの基底クラス
"""

import socket
import threading
import ipaddress
import random

from model import HachiUtil


class RandomPort:
    """ 範囲内のポート番号をランダムで返すクラス """

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __call__(self, * args):
        return random.randint(self.start, self.end)


class SendThread(threading.Thread):
    def __init__(self, params, counter):
        super(SendThread, self).__init__()
        self.unlimited = params.unlimited.get()
        self.freq = 1 / int(params.pps.get())
        self.payload = HachiUtil.ramdom_binary(int(params.datalen.get()))

        # 送信先アドレスリスト生成
        host = params.host.get()
        dstport_list = self._dstport_list(
            params.dstport_st.get(), params.dstport_ed.get(), params.dstport_type.get())
        self.address_list = [(host, port) for port in dstport_list]

        # srcportはIntVar()を渡す
        self.srcport_obj = params.srcport

        self.counter = counter
        self.stop_flg = False

        # IPv4とIPv6でソケットファミリー分かれる
        self.family = socket.AF_INET if ipaddress.ip_address(
            host).version == 4 else socket.AF_INET6

    def run(self):
        # 下位クラスで定義
        pass

    def stop(self):
        self.stop_flg = True

    def _dstport_list(self, start, end, _type):
        if _type == "単一":
            return [start]
        else:
            # 必ずdstport_stが小さくなるようにする
            if start > end:
                start, end = end, start

            if _type == "ﾗｳﾝﾄﾞﾛﾋﾞﾝ":
                return list(range(start, end+1))
            elif _type == "ランダム":
                return [RandomPort(start, end)()]
