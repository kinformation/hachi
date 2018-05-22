# -*- coding: utf-8 -*-

"""
UDPでパケットを投げるスレッド
"""

import socket
import time
from itertools import cycle, product
from contextlib import closing
# from struct import pack

from model import SendThread


class SendUdpThread(SendThread.SendThread):
    def __init__(self, params, sendObj, srcport):
        super().__init__(params, sendObj, srcport)

        # UDP送信用ソケット生成
        self.senddata = []  # (送信データ, 宛先アドレス)
        if params.advanced == False:  # 通常
            self.sock = socket.socket(self.family, socket.SOCK_DGRAM)
            # 宛先リスト分作成
            self.senddata = [(self.data, dst) for dst in self.dstaddr_list]
        else:  # 管理者権限
            self.sock = socket.socket(
                self.family, socket.SOCK_RAW, socket.IPPROTO_UDP)
            # self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 0)
            for dst, src in product(self.dstaddr_list, self.srcaddr_list):
                self.senddata.append((UDPPacket(self.data, dst, src), dst))

    def run(self):
        # 送信元ポート特定のため一発投げておく
        self.sock.sendto(self.senddata[0][0], self.senddata[0][1])
        self.srcport.set(self.sock.getsockname()[1])

        # with => ブロックを抜けるときに必ずsockのclose()が呼ばれる
        with closing(self.sock):
            # 最高速の処理を軽くするため処理を分ける
            if self.unlimited:
                self._send_u()
            else:
                self._send()

    def _send(self):
        # whileはforより圧倒的にループが遅い
        for (packet, address) in cycle(self.senddata):
            st = time.perf_counter()
            self.sock.sendto(packet, address)
            self.sendObj.count += 1
            if self.stop_flg:
                break

            # time.sleep(self.freq)は精度が低い
            # これで誤差はだいたい+1.5μ秒
            while time.perf_counter() - st < self.freq:
                pass

    def _send_u(self):
        for (packet, address) in cycle(self.senddata):
            self.sock.sendto(packet, address)
            self.sendObj.count += 1
            if self.stop_flg:
                break


from pypacker.layer3.ip import IP
from pypacker.layer3.ip6 import IP6
from pypacker.layer4.udp import UDP
import ipaddress


def UDPPacket(data, dst_addr, src_addr, **kwargs):
    """
    L3までのUDPパケットを生成する
    data -> binary
    dst_addr,src_addr -> (ip, port)
    """
    udp_header = UDP(sport=src_addr[1], dport=dst_addr[1], body_bytes=data)
    return udp_header.bin()
