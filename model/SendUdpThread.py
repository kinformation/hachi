# -*- coding: utf-8 -*-

"""
UDPでパケットを投げるスレッド
"""

import socket
import time
from itertools import repeat
from contextlib import closing

from model import SendThread


class SendUdpThread(SendThread.SendThread):
    def __init__(self, params, counter):
        super().__init__(params, counter)

        # UDP送信用ソケット生成
        self.sock = socket.socket(self.family, socket.SOCK_DGRAM)

    def run(self):
        # 送信元ポート特定のため一発投げておく
        print(self.address_list[0])
        print(self.address_list[0])
        self.sock.sendto(self.payload, self.address_list[0])
        self.srcport_obj.set(self.sock.getsockname()[1])

        # with => ブロックを抜けるときに必ずsockのclose()が呼ばれる
        with closing(self.sock):
            # 最高速の処理を軽くするため処理を分ける
            if self.unlimited:
                self._send_u()
            else:
                self._send()

    def _send(self):
        # whileはforより圧倒的にループが遅い
        st = 0
        size = len(self.address_list)
        for _ in repeat(0):
            st = time.perf_counter()
            self.sock.sendto(
                self.payload, self.address_list[self.counter.num % size])
            self.counter.num += 1
            if self.stop_flg:
                break

            # time.sleep(self.freq)は精度が低い
            # これで誤差はだいたい+1.5μ秒
            while time.perf_counter() - st < self.freq:
                pass

    def _send_u(self):
        size = len(self.address_list)
        for _ in repeat(0):
            self.sock.sendto(
                self.payload, self.address_list[self.counter.num % size])
            self.counter.num += 1
            if self.stop_flg:
                break
