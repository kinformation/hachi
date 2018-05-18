# -*- coding: utf-8 -*-

"""
UDPでパケットを投げるスレッド
"""

import socket
import time
from itertools import cycle
from contextlib import closing

from model import SendThread


class SendUdpThread(SendThread.SendThread):
    def __init__(self, params, counter):
        super().__init__(params, counter)

        # UDP送信用ソケット生成
        self.sock = socket.socket(self.family, socket.SOCK_DGRAM)

    def run(self):
        # 送信元ポート特定のため一発投げておく
        self.sock.sendto(self.payload, self.address_list[0])
        # self.srcport_obj.set(self.sock.getsockname()[1])

        # with => ブロックを抜けるときに必ずsockのclose()が呼ばれる
        with closing(self.sock):
            # 最高速の処理を軽くするため処理を分ける
            if self.unlimited:
                self._send_u()
            else:
                self._send()

    def _send(self):
        st = 0
        # whileはforより圧倒的にループが遅い
        for address in cycle(self.address_list):

            # stop_flg == True なら停止
            if self.stop_flg == True:
                break

            st = time.perf_counter()
            self.sock.sendto(self.payload, address)
            self.counter.num += 1

            # time.sleep(self.freq)は精度が低い
            # これで誤差はだいたい+1.5μ秒
            while time.perf_counter() - st < self.freq:
                pass

    def _send_u(self):
        for address in cycle(self.address_list):
            self.sock.sendto(self.payload, address)
            self.counter.num += 1
            if self.stop_flg:
                break
