# -*- coding: utf-8 -*-

"""
汎用ユーティリティ
"""

import string
import random
import netifaces
import ipaddress
import unicodedata


def ramdom_str(len):
    return ''.join([
        random.choice(string.ascii_letters + string.digits) for i in range(len)
    ])


def string_width(string):
    """
    文字列の見た目幅の長さを返す
    https://ymotongpoo.hatenablog.com/entry/20120511/1336706463
    """
    width = 0
    for c in string:
        char_width = unicodedata.east_asian_width(c)
        if char_width in u"WFA":
            width += 2
        else:
            width += 1
    return width


"""
ウィジェット用クラス
"""


class UpdateBps:
    """ bpsの動的更新 """

    def __init__(self, len, freq, bps_str):
        self.len = len
        self.freq = freq
        self.bps_str = bps_str

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
    """ ローカルIPアドレス(v4,v6)取得 """

    def __call__(self):
        list = []
        for ifname in netifaces.interfaces():
            ifaddr = netifaces.ifaddresses(ifname)
            # IPv4
            if netifaces.AF_INET in ifaddr:
                addr4 = ifaddr[netifaces.AF_INET][0]['addr']
                if self._check_addr(addr4) == True:
                    list.append(addr4)
            # IPv6
            if netifaces.AF_INET6 in ifaddr:
                addr6 = ifaddr[netifaces.AF_INET6][0]['addr']
                if self._check_addr(addr6) == True:
                    list.append(addr6)

        return list

    def _check_addr(self, addr):
        try:
            ip = ipaddress.ip_address(addr)
            # ループバックアドレスは除外
            return True if not ip.is_loopback else False
        except:
            # IPアドレス形式じゃなければ除外
            return False


class CheckUnlimited:
    """ 送信フィールドで"最高速"有効時に"送信パケット数/秒"非活性 """

    def __init__(self, check_flg, pps_obj):
        self.check_flg = check_flg
        self.pps_obj = pps_obj

    def __call__(self, * args):
        if self.check_flg.get():
            self.pps_obj.state(['disabled'])
        else:
            self.pps_obj.state(['!disabled'])
