# -*- coding: utf-8 -*-

"""
UDPでパケットを投げるスレッド
"""

import socket
import time
from itertools import cycle, product

from model import SendThread


class SendUdpThread(SendThread.SendThread):
    def __init__(self, params, sendObj, srcport):
        super().__init__(params, sendObj, srcport)

        # 送信元ポート分ソケット生成
        sock_list = []
        for srcaddr in self.srcaddr_list:
            sock = socket.socket(self.family, socket.SOCK_DGRAM)
            sock.bind((self.ZERO_IP, srcaddr[1]))
            sock_list.append(sock)

        # 送信元(socket)と送信先(address)の直積
        self.src_dst_list = list(product(sock_list, self.dstaddr_list))

    def run(self):
        # 最高速の処理を軽くするため処理を分ける
        if self.unlimited:
            self._send_u()
        else:
            self._send()

        # 全ソケット解放(TODO:例外で死んだときに有効か確認)
        for sock, _ in self.src_dst_list:
            sock.close()

    def _send(self):
        # whileはforより圧倒的にループが遅い
        for (src, dst) in cycle(self.src_dst_list):
            st = time.perf_counter()
            src.sendto(self.data, dst)
            self.sendObj.count += 1
            if self.stop_flg:
                break

            # time.sleep(self.freq)は精度が低い
            # これで誤差はだいたい+1.5μ秒
            while time.perf_counter() - st < self.freq:
                pass

    def _send_u(self):
        for (src, dst) in cycle(self.src_dst_list):
            src.sendto(self.data, dst)
            self.sendObj.count += 1
            if self.stop_flg:
                break
