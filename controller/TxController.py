# -*- coding: utf-8 -*-

from tkinter import messagebox
import ipaddress

from model import SendTcpThread, SendUdpThread, SendMonitorThread, HachiUtil
from controller import LogController


class SendcountShareObject(object):
    """ パケット送信数をスレッド間で共有するためのクラス """

    def __init__(self):
        self.num = 0


class SendAction:
    _instance = None

    def __new__(cls, params=None, widgets=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.params = params
            cls.widgets = widgets
            cls.stat = 0
            cls.sendcount = SendcountShareObject()

            # スレッド変数
            cls.th_send = None
            cls.th_monitor = None
        return cls._instance

    def __init__(self, params=None, widgets=None):
        pass

    def __call__(self, event=None):
        # 入力パラメータチェック
        msg = self._param_check()
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

        # パケット送信スレッド開始
        # 0:TCP
        # 1:UDP
        # 2:Original(不使用)
        proto = self.params.proto.get()
        host = self.params.host.get()
        dstport = self.params.dstport.get()
        if proto == 0:
            logger.insert("TCPパケット送信を開始します({}:{})".format(
                host, dstport))
            self._send_tcp_start()
        elif proto == 1:
            logger.insert("UDPパケット送信を開始します({}:{})".format(
                host, dstport))
            self._send_udp_start()
        elif proto == 2:
            pass

        # ウィジェット非活性化
        for widget in self.widgets.values():
            widget.state(['disabled'])

        self.stat = 1
        self.params.send_btn_text.set("送信停止")

    # TCPパケット送信スレッド
    def _send_tcp_start(self):
        self.th_send = SendTcpThread.SendTcpThread(self.params, self.sendcount)
        self.th_send.setDaemon(True)
        self.th_send.start()

    # UDPパケット送信スレッド
    def _send_udp_start(self):
        self.th_send = SendUdpThread.SendUdpThread(self.params, self.sendcount)
        self.th_send.setDaemon(True)
        self.th_send.start()

    # パケット送信監視スレッド
    def _monitor_start(self):
        self.th_monitor = SendMonitorThread.SendMonitorThread(
            self.sendcount, self.params.real_pps)
        self.th_monitor.setDaemon(True)
        self.th_monitor.start()

    # スレッド停止
    def _send_stop(self):
        LogController.LogController().insert("パケット送信を停止します")
        if self.th_send is not None:
            self.th_send.stop()
        if self.th_monitor is not None:
            self.th_monitor.stop()

        self.params.send_btn_text.set("送信開始")
        self.params.srcport.set("")
        # ウィジェット活性化
        for widget in self.widgets.values():
            widget.state(['!disabled'])

        # 無制限なら送信数Entryは非活性
        HachiUtil.CheckUnlimited(
            self.params.unlimited, self.widgets['entry_pps'])()

        self.stat = 0

    # パラメータチェック
    def _param_check(self):
        msg = ""
        host = self.params.host.get()
        dstport = self.params.dstport.get()
        datalen = self.params.datalen.get()
        pps = self.params.pps.get()

        # IPフォーマットチェック
        try:
            ipaddress.ip_address(host)
        except:
            # IPアドレス形式ではない
            msg += "・IPアドレスの指定が不正です。\n"

        # ポート番号 0～65535
        if dstport < 0 or 65535 < dstport:
            msg += "・ポート番号は 0～65535 の範囲で指定してください。\n"

        # データ長 0～9,000
        if datalen < 0 or 9000 < datalen:
            msg += "・データ長(byte)は 0～9,000 の範囲で指定してください。\n"

        # 送信パケット数/秒 1～20,000
        if pps < 1 or 20000 < pps:
            msg += "・送信パケット数/秒は 1～20,000 の範囲で指定してください。\n"

        return msg


def tcp_exception(exc_obj):
    logger = LogController.LogController()
    if len(exc_obj.args) == 1:
        msg = "コネクションの確立に失敗しました。"
    else:
        msg = exc_obj.args[1]
    logger.insert(msg)
    messagebox.showwarning(title="warning", message=msg)
    SendAction().send_stop()
