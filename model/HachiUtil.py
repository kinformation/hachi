# -*- coding: utf-8 -*-

"""
汎用ユーティリティ
"""

import struct
import random
import netifaces
import ipaddress


def ramdom_binary(len):
    """ 指定バイト数のランダムバイナリデータ生成 """
    return b''.join([struct.pack("B", random.randint(0, 255)) for i in range(0, len)])


"""
ウィジェット用クラス
"""


class UpdateBps:
    """ bpsの動的更新 """

    def __init__(self, len, freq, bps_str):
        self.len = len
        self.freq = freq
        self.bps_str = bps_str

        # 初回実行
        self()

    def __call__(self, *args):
        try:
            # 数値以外が設定されていたら例外へ飛ぶ
            bps = ((self.len.get() + 46) * 8) * self.freq.get()
            unit = " bps"

            if bps < 1024:
                unit = " bps"
            elif bps < pow(1024, 2):
                bps = int(bps/1024)
                unit = " Kbps"
            elif bps < pow(1024, 3):
                bps = int(bps/pow(1024, 2))
                unit = " Mbps"
            elif bps < pow(1024, 4):
                bps = round(bps/pow(1024, 3), 2)
                unit = " Gbps"

            self.bps_str.set(str(bps) + unit)

        except:
            self.bps_str.set("Unknown")


class LocalAddress:
    """ ローカルIPアドレス(v4,v6)管理 """

    def __init__(self):
        self.list = []
        for ifname in netifaces.interfaces():
            ifaddr = netifaces.ifaddresses(ifname)
            # IPv4
            if netifaces.AF_INET in ifaddr:
                addr4 = ifaddr[netifaces.AF_INET][0]['addr']
                if self._check_addr(addr4) == True:
                    self.list.append(addr4)
            # IPv6
            if netifaces.AF_INET6 in ifaddr:
                addr6 = ifaddr[netifaces.AF_INET6][0]['addr']
                if self._check_addr(addr6) == True:
                    self.list.append(addr6)

    def get(self):
        return self.list

    def is_localaddress(self, addr):
        return addr in self.list

    def _check_addr(self, addr):
        try:
            ip = ipaddress.ip_address(addr)
            # ループバックアドレスは除外
            return True if not ip.is_loopback else False
        except:
            # IPアドレス形式じゃなければ除外
            return False
