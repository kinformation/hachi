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


class ChangePortState:
    """ 送信先ポート(レンジ)ステータスの動的更新 """

    def __init__(self, type, entry):
        self.type = type
        self.entry = entry

    def __call__(self, *args):
        if self.type.get() == "単一":
            self.entry.state(['disabled'])
        else:
            self.entry.state(['!disabled'])


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

    def __call__(self):
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


class CheckUnlimited:
    """ 送信フィールドで"最高速"有効時に"送信パケット数/秒"非活性 """

    def __init__(self, check_variable, pps_obj):
        self.check_variable = check_variable
        self.pps_obj = pps_obj

    def __call__(self, * args):
        if self.check_variable.get():
            self.pps_obj.state(['disabled'])
        else:
            self.pps_obj.state(['!disabled'])


class ChangeSendProto:
    """ 送信プロトコル選択変更時の動作 """

    def __init__(self, proto, porttype, porttype_val):
        self.proto = proto
        self.porttype = porttype
        self.porttype_val = porttype_val

    def __call__(self, *args):
        # 送信プロトコル：UDP
        if self.proto.get() == 1:
            self.porttype.state(['!disabled'])
        # 送信プロトコル：UDP以外
        else:
            self.porttype_val.set('単一')
            self.porttype.state(['disabled'])
