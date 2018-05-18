
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
        return socket.inet_aton(socket.gethostbyname(name))

    def _get_checksum(self, data):
        """ チェックサムを生成 """

        result = 0
        # 2byte毎に１の補数変換して足し合わせる
        for i in range(0, len(data), 2):
            try:
                result += 0xffff - (data[i] << 8 | data[i+1])
            except IndexError:  # if len(data) % 2 != 0
                result += 0xffff - (data[i] << 8)

        # 下位16bitを１の補数変換
        result = (0xffff & result)
        print(hex(result))

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
    送信元ポート(16)+宛先ポート(16)+データ長(16)+チェックサム(16)+データ(任意)
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
    udp_header = pack(">HHH", src_addr[1], dst_addr[1], len(data)+8)

    # チェックサム用疑似ヘッダ(IPv4)
    pseudo_header = p.src + p.dst + b"\x00" + \
        p.protocol + pack(">H", 20+len(data))
    checksum_src = pseudo_header+udp_header+data.encode('utf-8')

    # チェックサム計算
    checksum = p._get_checksum(checksum_src)
    udp_header += pack(">H", checksum)

    p.data = udp_header+data.encode('utf-8')
    return p.build()


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
    # dont include ip header
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    # dst_addr, src_addr = ("127.0.0.1", 1234), ("127.0.0.1", 11112)
    dst_addr, src_addr = ("169.254.1.10", 12000), ("169.254.1.100", 12000)
    p = UDPPacket("testa", dst_addr, src_addr)
    s.sendto(p, dst_addr)
