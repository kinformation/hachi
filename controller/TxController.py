# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox
import ipaddress
import itertools
from functools import reduce
import re

from view import TxField
from model import SendTcpThread, SendUdpThread, SendIcmpThread, SendMonitorThread, HachiUtil
from controller import LogController

# =================================
# == 定数
# =================================
PROTO_TCP = 0
PROTO_UDP = 1
PROTO_ORG = 2
PROTO_ICMP = 3

DEF_PROTO = PROTO_UDP
DEF_DATALEN = 1024
DEF_PPS = 100
DEF_DST_IP = "169.254.1.80"
DEF_DST_PROT = 12000
DEF_SRC_IP = "169.254.1.80"
DEF_SRC_PROT = 12000

MIN_DATALEN = 0
MAX_DATALEN = 9999
MIN_PPS = 1
MAX_PPS = 20000

# =================================
# == 公開クラス
# =================================


class AddrVar:
    """ アドレス情報(IPアドレス,ポート)クラス """

    def __init__(self, ip=None, port=None):
        self.ip = tk.StringVar(value=ip)
        self.port = tk.StringVar(value=port)

    def address_list(self):
        return list(itertools.product(self.ip_list(), self.port_list()))

    def ip_list(self):
        return self._purse_ip(self.ip.get())

    def port_list(self):
        return self._purse_port(self.port.get())

    def _purse_ip(self, str):
        # "1,2" => ['1', '2']
        # "1-3" => ['1', '2', '3']
        # "1,2,4-6" => ['1', '2', '4', '5', '6']
        li = str.split(",")

        # 重複削除
        li_uniq = list(set(li))

        return li_uniq

    def _purse_port(self, str):
        # 入力値展開
        li = self._expand_num(str)

        # ソート、重複削除
        return sorted(list(set(li)))

    def _expand_num(self, s):
        # カンマで分割、ハイフンを展開
        # 正の整数のみ許容。不正入力は-1で出力
        # -----------------------
        # [OKパターン]
        #   "1,2" => [1, 2]
        #   "1-3" => [1, 2, 3]
        #   "1,3-5,7" => [1, 3, 4, 5, 7]
        # [NGパターン]
        #   "1,a" => [1, -1]
        #   "1,a-5" => [1, -1]
        #   "1-b" => [-1]
        #   "1-" => [-1]
        #   "-7" => [-1]
        # -----------------------

        a = re.split(", *", s)
        r = re.compile("[0-9]+-[0-9]+")

        def f(s1):
            a, b = map(int, s1.split('-'))
            return list(range(a, b+1))

        def g(x):
            if r.match(x):
                return f(x)
            else:
                return [int(x) if x.isdecimal() else -1]

        return reduce(lambda x, y: x + g(y), a, [])


class SendParams(object):
    """ 送信パラメータ情報クラス """

    _instance = None

    def __new__(cls, *args, **keys):
        if cls._instance is None:
            cls._instance = object.__new__(cls)

            cls.proto = tk.IntVar(value=DEF_PROTO)
            cls.datalen = tk.StringVar(value=DEF_DATALEN)
            cls.pps = tk.StringVar(value=DEF_PPS)
            cls.unlimited = tk.BooleanVar(value=False)
            cls.bps = tk.StringVar()
            cls.dstaddr = AddrVar(ip=DEF_DST_IP, port=DEF_DST_PROT)
            cls.srcaddr = AddrVar(port=DEF_SRC_PROT)
            cls.advanced = HachiUtil.is_admin()

            # "bps目安"動的更新
            bps_callback = HachiUtil.UpdateBps(cls.datalen, cls.pps, cls.bps)
            cls.pps.trace_add('write', bps_callback)
            cls.datalen.trace_add('write', bps_callback)

        return cls._instance


class MonitorParams(object):
    """ 送信モニター情報クラス """

    _instance = None

    def __new__(cls, *args, **keys):
        if cls._instance is None:
            cls._instance = object.__new__(cls)

            cls.bps = tk.StringVar()
            cls.datalen = tk.IntVar()
            cls.pps = tk.IntVar()
            cls.srcport = tk.StringVar()
            cls.send_btn = tk.StringVar(value="送信開始")

            # "bps換算"動的更新
            cls.pps.trace_add('write', HachiUtil.UpdateBps(
                cls.datalen, cls.pps, cls.bps))

        return cls._instance


class SendShareObject(object):
    """ スレッド間でデータを共有するためのクラス """

    def __init__(self):
        self.count = 0


class SendAction:
    """ 送信ボタン押下時の動作設定 """

    _instance = None

    def __new__(cls, widgets=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.widgets = widgets
            cls.sendParams = SendParams()
            cls.monitorParams = MonitorParams()

            cls.stat = 0
            cls.sendObj = SendShareObject()

            # スレッド変数
            cls.th_send = None
            cls.th_monitor = None

        return cls._instance

    def __call__(self, event=None):
        # 入力パラメータチェック
        msg = _param_check()
        if len(msg) > 0:
            messagebox.showwarning(title="warning", message=msg)
            return

        if self.stat == 0:
            self._send_start()
        else:
            self._send_stop()

    def send_stop(self):
        self._send_stop()

    def _send_start(self):
        # ログ出力インスタンス
        logger = LogController.LogController()

        # モニタースレッド開始
        self._monitor_start()

        # モニターデータ長セット
        MonitorParams.datalen.set(SendParams.datalen.get())

        # パケット送信スレッド開始
        #   0:TCP 1:UDP 2:Original(不使用) 3:ICMP
        proto = SendParams.proto.get()
        if proto == PROTO_TCP:
            logger.insert("TCPパケット送信を開始します\n{}".format(
                SendParams.dstaddr.address_list()))
            self._send_tcp_start()
        elif proto == PROTO_UDP:
            logger.insert("UDPパケット送信を開始します\n{}".format(
                SendParams.dstaddr.address_list()))
            self._send_udp_start()
        elif proto == PROTO_ORG:
            pass
        elif proto == PROTO_ICMP:
            logger.insert("ICMPパケット送信を開始します\n{}".format(
                SendParams.dstaddr.address_list()))
            self._send_icmp_start()

        MonitorParams.send_btn.set("送信停止")

        # ウィジェット非活性化
        for widget in self.widgets.values():
            widget.state(['disabled'])

        self.stat = 1

    def _send_tcp_start(self):
        """ TCPパケット送信スレッド """

        self.th_send = SendTcpThread.SendTcpThread(
            SendParams(), self.sendObj, MonitorParams().srcport)
        self.th_send.setDaemon(True)
        self.th_send.start()

    def _send_udp_start(self):
        """ UDPパケット送信スレッド """

        self.th_send = SendUdpThread.SendUdpThread(
            SendParams(), self.sendObj, MonitorParams().srcport)
        self.th_send.setDaemon(True)
        self.th_send.start()

    def _send_icmp_start(self):
        """ ICMPパケット送信スレッド """

        self.th_send = SendIcmpThread.SendIcmpThread(
            SendParams(), self.sendObj, MonitorParams().srcport)
        self.th_send.setDaemon(True)
        self.th_send.start()

    def _monitor_start(self):
        """ パケット送信監視スレッド """

        self.th_monitor = SendMonitorThread.SendMonitorThread(
            self.sendObj, MonitorParams())
        self.th_monitor.setDaemon(True)
        self.th_monitor.start()

    # スレッド停止
    def _send_stop(self):
        LogController.LogController().insert("パケット送信を停止します")

        # スレッド停止
        if self.th_send is not None:
            self.th_send.stop()
        if self.th_monitor is not None:
            self.th_monitor.stop()

        MonitorParams.srcport.set("")
        MonitorParams.datalen.set(0)
        MonitorParams.send_btn.set("送信開始")

        # ウィジェット活性化
        for widget in self.widgets.values():
            widget.state(['!disabled'])

        # 無制限なら送信数Entryは非活性
        CheckUnlimited(
            SendParams.unlimited, self.widgets['param_pps'])()

        # ICMPなら送信元/送信先ポート番号非活性
        ChangeProtocol(
            SendParams.proto, self.widgets['srcport'], self.widgets['dstport'])()

        # # 管理者権限モード表示設定(管理者権限モードなし)
        # advanced_view(self.widgets)

        self.stat = 0


class CheckUnlimited:
    """ 「最高速」チェック時の動作設定 """

    def __init__(self, check_variable, pps_obj):
        self.check_variable = check_variable
        self.pps_obj = pps_obj

    def __call__(self, * args):
        # チェック時に"送信パケット数/秒"非活性
        if self.check_variable.get():
            self.pps_obj.state(['disabled'])
        else:
            self.pps_obj.state(['!disabled'])


class ChangeProtocol:
    """ 「使用プロトコル」変更時の動作設定 """

    def __init__(self, select_variable, srcport_obj, dstport_obj):
        self.select_variable = select_variable
        self.srcport_obj = srcport_obj
        self.dstport_obj = dstport_obj

    def __call__(self, * args):
        proto = self.select_variable.get()

        # ICMPなら送信元/送信先ポート番号非活性
        if proto == PROTO_ICMP:
            self.srcport_obj.state(['disabled'])
            self.dstport_obj.state(['disabled'])
        else:
            self.srcport_obj.state(['!disabled'])
            self.dstport_obj.state(['!disabled'])

# =================================
# == 公開関数
# =================================


def tcp_exception(exc_obj):
    logger = LogController.LogController()
    if len(exc_obj.args) == 1:
        msg = "コネクションの確立に失敗しました。"
    else:
        msg = exc_obj.args[1]
    logger.insert(msg)
    messagebox.showwarning(title="warning", message=msg)
    SendAction().send_stop()


def advanced_view(widgets):
    """ 管理者権限モードの動作設定 """

    srcip_obj = widgets['srcip']
    srcport_obj = widgets['srcport']

    # 通常モード
    if HachiUtil.is_admin() == False:
        srcip_obj.state(['disabled'])
        srcport_obj.state(['disabled'])
    # 管理者権限モード
    else:
        srcip_obj.state(['!disabled'])
        srcport_obj.state(['!disabled'])

# =================================
# == ローカル関数
# =================================


def _param_check():
    """ 送信パラメータチェック """

    msg = ""
    dstaddr = SendParams.dstaddr
    srcaddr = SendParams.srcaddr
    datalen = SendParams.datalen.get()
    proto = SendParams.proto.get()
    pps = SendParams.pps.get()

    # 送信先IPフォーマットチェック
    dstip_list = dstaddr.ip_list()
    if proto == PROTO_TCP and len(dstip_list) >= 2:  # TCPプロトコルかつ、複数指定
        msg += "・TCPプロトコルで複数の送信先IPアドレスは指定できません。\n"
    else:
        try:
            for ip in dstip_list:
                ipaddress.ip_address(ip)
        except:
            # IPアドレス形式ではない
            msg += "・送信先IPアドレスの指定が不正です。\n"

    # 送信先ポート番号 0～65535
    dstport_list = dstaddr.port_list()
    if proto == PROTO_TCP and len(dstport_list) >= 2:  # TCPプロトコルかつ、複数指定
        msg += "・TCPプロトコルで複数の送信先ポート番号は指定できません。\n"
    else:
        for port in dstport_list:
            if not (0 <= port <= 65535):
                msg += "・送信先ポート番号は 0～65535 の範囲で指定してください。\n"
                break

    # # 送信元IPフォーマットチェック
    # # TODO:送信元IPアドレス設定不可
    # try:
    #     for ip in srcaddr.ip_list():
    #         ipaddress.ip_address(ip)
    # except:
    #     # IPアドレス形式ではない
    #     msg += "・送信元IPアドレスの指定が不正です。\n"

    # 送信元ポート番号 0～65535
    srcport_list = srcaddr.ip_list()
    if proto == PROTO_TCP and len(srcport_list) >= 2:  # TCPプロトコルかつ、複数指定
        msg += "・TCPプロトコルで複数の送信元ポート番号は指定できません。\n"
    else:
        for port in srcaddr.port_list():
            if not (0 <= int(port) <= 65535):
                msg += "・送信元ポート番号は 0～65535 の範囲で指定してください。\n"
                break

    # データ長
    if not (datalen.isdigit() and (MIN_DATALEN <= int(datalen) <= MAX_DATALEN)):
        msg += "・データ長(byte)は {}～{} の範囲で指定してください。\n".format(MIN_DATALEN, MAX_DATALEN)

    # 送信パケット数/秒
    if not (pps.isdigit() and (MIN_PPS <= int(pps) <= MAX_PPS)):
        msg += "・送信パケット数/秒は {}～{} の範囲で指定してください。\n".format(MIN_PPS, MAX_PPS)

    return msg
