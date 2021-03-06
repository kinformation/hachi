# -*- coding: utf-8 -*-

"""
汎用ユーティリティ
"""

from struct import pack
from random import randint
import netifaces
import ipaddress
import ctypes

# =================================
# == 公開関数
# =================================


def ramdom_binary(len):
    """ 指定バイト数のランダムバイナリデータ生成 """
    return b''.join([pack("B", randint(0, 255)) for i in range(0, len)])


def is_admin():
    """ 管理者権限で実行かチェック """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


# =================================
# == 公開クラス
# == ウィジェット用
# =================================

class UpdateBps:
    """ bpsの動的更新 """

    def __init__(self, len, pps, bps_str):
        self.len = len
        self.pps = pps
        self.bps_str = bps_str

        # 初回実行
        self()

    def __call__(self, *args):
        try:
            # 数値以外が設定されていたら例外へ飛ぶ
            len = int(self.len.get())
            pps = int(self.pps.get())

            HEADER_LEN = 46
            BYTE_2_BIT = 8

            bps = (len+HEADER_LEN) * BYTE_2_BIT * pps
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
                for ipv4 in ifaddr[netifaces.AF_INET]:
                    if self._check_addr(ipv4['addr']) == True:
                        self.list.append(ipv4['addr'])
            # IPv6
            if netifaces.AF_INET6 in ifaddr:
                for ipv6 in ifaddr[netifaces.AF_INET6]:
                    if self._check_addr(ipv6['addr']) == True:
                        self.list.append(ipv6['addr'])

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
