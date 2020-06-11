# -*- coding: utf-8 -*-

import socket
import time
from itertools import cycle, product

from model import SendThread


class SendIcmpThread(SendThread.SendThread):
    """ ICMPパケットを投げるスレッド """

    def __init__(self, params, sendObj, srcport):
        super().__init__(params, sendObj, srcport)

        # 送信元ポート分ソケット生成
        sock_list = []
        sock = socket.socket(
            socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        sock_list.append(sock)

        # 送信元(socket)と送信先(address)の直積
        self.src_dst_list = list(product(sock_list, self.dstaddr_list))

        # ICMPパケット構築
        p = [0]*8
        p[0] = (0x08)  # Type
        p[1] = (0x00)  # Code
        p[2] = 0       # Checksum1
        p[3] = 0       # Checksum2
        p[4] = (0x00)  # Identifier1
        p[5] = (0x01)  # Identifier2
        p[6] = (0x00)  # Sequence1
        p[7] = (0x01)  # Sequence2
        p.extend(self.data)

        # チェックサム計算
        csum = 0
        for i in range(int(len(p)/2)):
            csum += (p[i*2] << 8) | (p[i*2+1])
        csum = (csum & 0xffff) + (csum >> 16)
        csum = 0xffff-(csum)
        p[2] = (csum & 0xFF00) >> 8
        p[3] = csum & 0x00FF

        self.packet = bytes(p)

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

        for (src, dst) in cycle(self.src_dst_list):
            st = time.perf_counter()
            src.sendto(self.packet, (dst[0], 0))

            self.sendObj.count += 1
            if self.stop_flg:
                break

            # time.sleep(self.freq)は精度が低い
            # これで誤差はだいたい+1.5μ秒
            while time.perf_counter() - st < self.freq:
                pass

    def _send_u(self):
        for (src, dst) in cycle(self.src_dst_list):
            src.sendto(self.packet, (dst[0], 0))
            self.sendObj.count += 1
            if self.stop_flg:
                break
