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
    def __init__(self, params, sendObj, srcport):
        super().__init__(params, sendObj, srcport)

        # UDP送信用ソケット生成
        # self.sock = socket.socket(self.family, socket.SOCK_DGRAM)
        self.sock = socket.socket(
            self.family, socket.SOCK_RAW, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        # dst_addr, src_addr = ("127.0.0.1", 1234), ("127.0.0.1", 11112)
        dst_addr, src_addr = self.address_list[0], ("169.254.1.100", 52321)
        self.payload = UDPPacket("abbaaaaaa", dst_addr, src_addr)

    def run(self):
        # 送信元ポート特定のため一発投げておく
        self.sock.sendto(self.payload, self.address_list[0])
        self.srcport.set(self.sock.getsockname()[1])

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
            st = time.perf_counter()
            self.sock.sendto(self.payload, address)
            self.sendObj.count += 1
            if self.stop_flg:
                break

            # time.sleep(self.freq)は精度が低い
            # これで誤差はだいたい+1.5μ秒
            while time.perf_counter() - st < self.freq:
                pass

    def _send_u(self):
        for address in cycle(self.address_list):
            self.sock.sendto(self.payload, address)
            self.sendObj.count += 1
            if self.stop_flg:
                break

# --------------------------------------------------


# -*- coding: utf-8 -*-
import socket
from struct import pack
import random


class Packet:
    def __init__(self):
        self.version = 4  # ip version
        self.hl = 5  # internet header length
        self.tos = 0  # type of service
        # self.length = 0 #length
        self.id = 41407  # identification
        self.flags = 0b010  # reserved+don't fragment(df)+more fragments(mf)
        self.offset = 0  # fragment offset
        self.ttl = 128  # time to live
        self.protocol = 255  # ip protocol raw: 255
        self.checksum = 0  # header checksum
        self.src = b"\x7f\x00\x00\x01"  # source ip address
        self.dst = b"\x7f\x00\x00\x01"  # destination ip address
        self.data = ""

    def _get_addr(self, name):
        # return socket.inet_aton(socket.gethostbyname(name))
        return socket.inet_aton(name)

    def _get_checksum(self, data):
        """ チェックサムを生成 """

        result = 0
        # 1. 2オクテットごとに足し合わせる(奇数なら\x00パディング)
        for i in range(0, len(data), 2):
            try:
                result += data[i] << 8 | data[i+1]
            except IndexError:  # 奇数オクテットの場合
                result += data[i] << 8

        # 2. LSB(下位16bit)とMSB(上位16bit:桁あふれ分)を加算する
        while result > 0xffff:
            result = (result & 0xffff)+(result >> 16)

        # 3. 計算結果の１の補数を返す
        result = 0xffff - result

        return result

    def set_src(self, name):
        self.src = self._get_addr(name)

    def set_dst(self, name):
        self.dst = self._get_addr(name)

    def build(self):
        """ IPパケット構築 """

        length = self.hl*4+len(self.data)
        result = b""
        result += ((self.version << 4)+self.hl).to_bytes(1, 'big')
        result += self.tos.to_bytes(1, 'big')
        result += pack(">H", length)
        result += pack(">H", self.id)
        result += pack(">H", (self.flags << 13)+self.offset)
        result += self.ttl.to_bytes(1, 'big')
        result += self.protocol
        result += b"\x00\x00"
        result += self.src+self.dst+self.data
        return result


def UDPPacket(data, dst_addr, src_addr, **kwargs):
    """
    UDPパケットを生成する
    """

    p = Packet()

    for attr, value in kwargs.items():
        setattr(p, attr, value)

    # プロトコル番号(UDP:17)設定
    p.protocol = b"\x11"
    # 送信元IPアドレス設定
    p.set_src(src_addr[0])
    # 送信先IPアドレス設定
    p.set_dst(dst_addr[0])

    # UDPヘッダ
    #  0      7 8     15 16    23 24    31
    # +--------+--------+--------+--------+
    # |   source port   | destination port|
    # +--------+--------+--------+--------+
    # |     length      |    checksum     |
    # +--------+--------+--------+--------+
    # |               data
    # +---------------- ...
    udp_header = pack(">HHH", src_addr[1], dst_addr[1], len(data)+8)

    # チェックサム用疑似ヘッダ(IPv4)
    #  0      7 8     15 16    23 24    31
    # +--------+--------+--------+--------+
    # |          source address           |
    # +--------+--------+--------+--------+
    # |        destination address        |
    # +--------+--------+--------+--------+
    # |  zero  |protocol|   UDP length    |
    # +--------+--------+--------+--------+
    # pseudo_len = (1).to_bytes(2, 'big')
    pseudo_len = (8 + len(data)).to_bytes(2, 'big')
    pseudo_header = p.src + p.dst + b"\x00" + p.protocol + pseudo_len
    checksum_src = pseudo_header+udp_header+data.encode('utf-8')

    # チェックサム計算
    checksum = p._get_checksum(checksum_src)
    # udp_header += checksum.to_bytes(2, 'big')
    udp_header += pack(">H", checksum)

    p.data = udp_header+data.encode('utf-8')
    return p.build()


# if __name__ == "__main__":
#     s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
#     # dont include ip header
#     s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

#     # dst_addr, src_addr = ("127.0.0.1", 1234), ("127.0.0.1", 11112)
#     dst_addr, src_addr = ("192.168.2.202", 12000), ("192.168.2.101", 52321)
#     p = UDPPacket("abbaaaaaa", dst_addr, src_addr)
#     s.sendto(p, dst_addr)
