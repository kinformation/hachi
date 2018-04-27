# -*- coding: utf-8 -*-

from tkinter import messagebox
import ipaddress

from model import RecvTcpThread, RecvUdpThread, RecvMonitorThread
from controller import LogController


class RecvShareObject(object):
    """ スレッド間で値を共有するためのクラス """

    def __init__(self):
        self.count = 0
        self.total = 0


class RecvAction:
    def __init__(self, params, widgets):
        self.proto = params.proto
        self.host = params.host
        self.port = params.port
        self.real_pps = params.real_pps
        self.real_datalen = params.real_datalen
        self.recv_btn_text = params.recv_btn_text
        self.widgets = widgets
        self.stat = 0

        self.share_obj = RecvShareObject()

        # スレッド変数
        self.th_recv = None
        self.th_monitor = None

    def __call__(self, event=None):

        ret, msg = self._param_check()
        if ret == False:
            messagebox.showwarning(title="warning", message=msg)
            return

        if self.stat == 0:
            self.monitor_start()

            # 0:TCP
            # 1:UDP
            if self.proto.get() == 0:
                self.recv_tcp_start()
            elif self.proto.get() == 1:
                self.recv_udp_start()
            for widget in self.widgets.values():
                widget.state(['disabled'])
            self.stat = 1
            self.recv_btn_text.set("受信停止")
        else:
            self.recv_stop()

    # TCPパケット送信スレッド
    def recv_tcp_start(self):
        LogController.LogController().insert(
            "TCPパケット受信を開始します({}:{})".format(self.host.get(), self.port.get()))
        self.th_recv = RecvTcpThread.RecvTcpThread(
            self.host.get(), self.port.get(), self.share_obj)
        self.th_recv.setDaemon(True)
        self.th_recv.start()

    # UDPパケット受信スレッド
    def recv_udp_start(self):
        LogController.LogController().insert(
            "UDPパケット受信を開始します({}:{})".format(self.host.get(), self.port.get()))
        self.th_recv = RecvUdpThread.RecvUdpThread(
            self.host.get(), self.port.get(), self.share_obj)
        self.th_recv.setDaemon(True)
        self.th_recv.start()

    # パケット受信監視スレッド
    def monitor_start(self):
        self.th_monitor = RecvMonitorThread.RecvMonitorThread(
            self.share_obj, self.real_datalen, self.real_pps)
        self.th_monitor.setDaemon(True)
        self.th_monitor.start()

    # スレッド停止
    def recv_stop(self):
        LogController.LogController().insert("パケット受信を停止します")

        self.th_recv.stop()
        self.th_monitor.stop()

        self.recv_btn_text.set("受信開始")
        # 設定ウィジェット活性化
        for widget in self.widgets.values():
            widget.state(['!disabled'])
        self.stat = 0

    # パラメータチェック
    def _param_check(self):
        ret = True
        msg = ""

        # IPフォーマットチェック
        try:
            ipaddress.ip_address(self.host.get())
        except:
            # IPアドレス形式ではない
            msg += "・IPアドレスの指定が不正です。\n"
            ret = False

        # ポート番号 0～65535
        if self.port.get() < 0 or 65535 < self.port.get():
            msg += "・ポート番号は 0～65535 の範囲で指定してください。\n"
            ret = False

        return ret, msg
