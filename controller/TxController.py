# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox
import ipaddress
import itertools

from view import TxField
from model import SendTcpThread, SendUdpThread, SendMonitorThread, HachiUtil
from controller import LogController

# =================================
# == 定数
# =================================
DEF_PROTO = 1  # 0:TCP 1:UDP
DEF_DATALEN = 1024
DEF_PPS = 100
DEF_DST_IP = "169.254.1.80"
DEF_DST_PROT = 12000

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
        return self._purse(self.ip.get())

    def port_list(self):
        # リスト全要素をint型に変換して返す
        return list(map(int, self._purse(self.port.get())))

    def _purse(self, str):
        # "1,2" => ['1', '2']
        # "1-3" => ['1', '2', '3']
        # "1,2,4-6" => ['1', '2', '4', '5', '6']
        return str.split(",")


class SendParams(object):
    """ 送信パラメータ情報クラス """

    _instance = None

    def __new__(cls, *args, **keys):
        if cls._instance is None:
            cls._instance = object.__new__(cls)

            cls.proto = tk.IntVar(value=DEF_PROTO)
            cls.datalen = tk.IntVar(value=DEF_DATALEN)
            cls.pps = tk.IntVar(value=DEF_PPS)
            cls.unlimited = tk.BooleanVar(value=False)
            cls.bps = tk.StringVar()
            cls.dstaddr = AddrVar(ip=DEF_DST_IP, port=DEF_DST_PROT)
            cls.srcaddr = AddrVar()

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


class SendcountShareObject(object):
    """ パケット送信数をスレッド間で共有するためのクラス """

    def __init__(self):
        self.num = 0


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
            cls.sendcount = SendcountShareObject()

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

#     def send_stop(self):
#         self._send_stop()

    def _send_start(self):
        # ログ出力インスタンス
        logger = LogController.LogController()

        # モニタースレッド開始
        self._monitor_start()

        # モニターデータ長セット
        MonitorParams.datalen.set(SendParams.datalen.get())

        # パケット送信スレッド開始
        #   0:TCP 1:UDP 2:Original(不使用)
        proto = SendParams.proto.get()
        if proto == 0:
            logger.insert("TCPパケット送信を開始します\n{}".format(
                SendParams.dstaddr.address_list()))
            self._send_tcp_start()
        elif proto == 1:
            logger.insert("UDPパケット送信を開始します\n{}".format(
                SendParams.dstaddr.address_list()))
            self._send_udp_start()
        elif proto == 2:
            pass

        MonitorParams.send_btn.set("送信停止")

        # ウィジェット非活性化
        for widget in self.widgets.values():
            widget.state(['disabled'])

        self.stat = 1

    def _send_tcp_start(self):
        """ TCPパケット送信スレッド """

        self.th_send = SendTcpThread.SendTcpThread(
            SendParams(), self.sendcount)
        self.th_send.setDaemon(True)
        self.th_send.start()

    def _send_udp_start(self):
        """ UDPパケット送信スレッド """

        self.th_send = SendUdpThread.SendUdpThread(
            SendParams(), self.sendcount)
        self.th_send.setDaemon(True)
        self.th_send.start()

    def _monitor_start(self):
        """ パケット送信監視スレッド """

        self.th_monitor = SendMonitorThread.SendMonitorThread(
            self.sendcount, MonitorParams.pps)
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

        self.stat = 0


# def tcp_exception(exc_obj):
#     logger = LogController.LogController()
#     if len(exc_obj.args) == 1:
#         msg = "コネクションの確立に失敗しました。"
#     else:
#         msg = exc_obj.args[1]
#     logger.insert(msg)
#     messagebox.showwarning(title="warning", message=msg)
#     SendAction().send_stop()


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


# =================================
# == ローカル関数
# =================================
def _param_check():
    """ 送信パラメータチェック """

    msg = ""
    dstaddr = SendParams.dstaddr
    datalen = SendParams.datalen.get()
    pps = SendParams.pps.get()

    # IPフォーマットチェック
    try:
        for ip in dstaddr.ip_list():
            ipaddress.ip_address(ip)
    except:
        # IPアドレス形式ではない
        msg += "・IPアドレスの指定が不正です。\n"

    # ポート番号 0～65535
    for port in dstaddr.port_list():
        if not (0 <= port <= 65535):
            msg += "・ポート番号は 0～65535 の範囲で指定してください。\n"

    # データ長
    if not (MIN_DATALEN <= datalen <= MAX_DATALEN):
        msg += "・データ長(byte)は {}～{} の範囲で指定してください。\n".format(MIN_DATALEN, MAX_DATALEN)

    # 送信パケット数/秒
    if not (MIN_DATALEN <= pps <= MAX_PPS):
        msg += "・送信パケット数/秒は {}～{} の範囲で指定してください。\n".format(MIN_DATALEN, MAX_PPS)

    return msg
