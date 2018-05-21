# -*- coding: utf-8 -*-

"""
UDPでパケットを投げるスレッド
"""

import socket
import time
from itertools import cycle, product
from contextlib import closing
from struct import pack

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
            self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
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
        self.src = self._get_addr('127.0.0.1')  # source ip address
        self.dst = self._get_addr('127.0.0.1')  # destination ip address
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
        return 0xffff - result

    def set_src(self, name):
        self.src = self._get_addr(name)

    def set_dst(self, name):
        self.dst = self._get_addr(name)

    def build(self):
        """ IPパケット構築 """

        length = self.hl*4+len(self.data)
        result = b""
        result += pack(">B", (self.version << 4)+self.hl)
        result += pack(">B", self.tos)
        result += pack(">H", length)
        result += pack(">H", self.id)
        result += pack(">H", (self.flags << 13)+self.offset)
        result += pack(">B", self.ttl)
        result += pack(">B", self.protocol)
        result += pack(">H", 0)
        result += self.src+self.dst+self.data
        return result


def UDPPacket(data, dst_addr, src_addr, **kwargs):
    """
    UDPパケットを生成する
    data -> binary
    dst_addr,src_addr -> (ip, port)
    """

    p = Packet()

    for attr, value in kwargs.items():
        setattr(p, attr, value)

    # プロトコル番号設定
    p.protocol = 17

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
    pseudo_len = pack(">H", (len(data)+8))
    pseudo_header = p.src + p.dst + b"\x00" + \
        pack(">B", p.protocol) + pseudo_len
    checksum_src = pseudo_header+udp_header+data

    # チェックサム計算
    checksum = p._get_checksum(checksum_src)
    udp_header += pack(">H", checksum)

    p.data = udp_header+data
    return p.build()
