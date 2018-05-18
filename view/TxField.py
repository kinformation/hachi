# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk

from view import Common
from controller import TxController

# =================================
# == グローバル変数
# =================================
txWidgets = {}

# =================================
# == 送信領域表示設定
# =================================


class SettingField(ttk.LabelFrame):
    """ 送信設定フィールド """

    def __init__(self, master):
        ttk.LabelFrame.__init__(self, master, text="送信設定")

        # プロトコル設定(1列目)
        ProtocolField(self).pack()
        # 送信先設定(2列目)
        DstAddressField(self).pack()
        # 送信元設定(3列目)
        # SrcAddressField(self).pack()
        # 送信パラメータ設定(4列目)
        SendParamField(self).pack()


class ProtocolField(ttk.LabelFrame):
    """ 使用プロトコルフィールド """

    def __init__(self, master):
        ttk.LabelFrame.__init__(self, master, text="使用プロトコル")

        # プロトコルリスト
        radio_item = {
            'proto_tcp': {'text': "TCP", 'value': 0},
            'proto_udp': {'text': "UDP", 'value': 1},
            # originalは使わなさそうなので除外
            # 'proto_org': {'text': "Original", 'value': 2},
        }

        for key, val in radio_item.items():
            item = ttk.Radiobutton(
                self, text=val['text'], value=val['value'])
            item.configure(variable=TxController.SendParams().proto)
            item.pack(side=tk.LEFT, padx=8)
            txWidgets[key] = item


class DstAddressField(ttk.LabelFrame):
    """ 送信先設定フィールド """

    def __init__(self, master):
        ttk.LabelFrame.__init__(self, master, text="送信先設定")

        # IPアドレス
        dstip = Common.LabelEntry(self, text="IPアドレス", width=30)
        dstip.Entry.configure(
            textvariable=TxController.SendParams().dstaddr.ip)
        dstip.pack(side=tk.LEFT, anchor=tk.N)
        txWidgets['dstip'] = dstip.Entry

        # ポート番号
        dstport = Common.LabelEntry(self, text="ポート番号", width=20)
        dstport.Entry.configure(
            textvariable=TxController.SendParams().dstaddr.port)
        dstport.pack(anchor=tk.N)
        txWidgets['dstport'] = dstport.Entry


class SrcAddressField(ttk.LabelFrame):
    """ 送信元設定フィールド """

    def __init__(self, master):
        ttk.LabelFrame.__init__(self, master, text="送信元設定")

        # IPアドレス
        srcip = Common.LabelEntry(self, text="IPアドレス", width=30)
        srcip.Entry.configure(
            textvariable=TxController.SendParams().srcaddr.port)
        srcip.pack(side=tk.LEFT, anchor=tk.N)
        txWidgets['srcip'] = srcip.Entry

        # ポート番号
        srcport = Common.LabelEntry(self, text="ポート番号", width=20)
        srcport.Entry.configure(
            textvariable=TxController.SendParams().srcaddr.port)
        srcport.pack(anchor=tk.N)
        txWidgets['srcport'] = srcport.Entry


class SendParamField(ttk.Frame):
    """ 送信パラメータフィールド """

    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        # データ長
        param_datalen = Common.LabelEntry(self, text="データ長", width=6)
        param_datalen.pack(side=tk.LEFT)
        param_datalen.Entry.configure(
            textvariable=TxController.SendParams().datalen)
        txWidgets['param_datalen'] = param_datalen.Entry

        # 送信パケット数/秒
        param_pps = Common.LabelEntry(self, text="送信パケット数/秒", width=6)
        param_pps.pack(side=tk.LEFT)
        param_pps.Entry.configure(textvariable=TxController.SendParams().pps)
        txWidgets['param_pps'] = param_pps.Entry

        # 最高速
        param_unlimited = ttk.Checkbutton(self, text='最高速')
        param_unlimited.pack(side=tk.LEFT)
        param_unlimited.configure(command=TxController.CheckUnlimited(
            TxController.SendParams().unlimited, txWidgets['param_pps']))
        param_unlimited.configure(variable=TxController.SendParams().unlimited)
        txWidgets['param_unlimited'] = param_unlimited

        # # 送信速度の目安
        # ttk.Label(self, text="送信速度の目安:   ").pack(side=tk.LEFT)
        # txWidgets['param_pps'] = param_pps


class MonitorField(ttk.LabelFrame):
    """ 送信モニターフィールド """

    def __init__(self, master):
        ttk.LabelFrame.__init__(self, master, text="送信モニター")

        # 送信数/秒
        mon_pps = Common.LabelReadonlyEntry(self, text="送信数/秒", width=7)
        mon_pps.Entry.configure(textvariable=TxController.MonitorParams().pps)

        # データ長(Byte)
        mon_datalen = Common.LabelReadonlyEntry(
            self, text="データ長(Byte)", width=6)
        mon_datalen.Entry.configure(
            textvariable=TxController.MonitorParams().datalen)

        # bps換算
        mon_bps = Common.LabelReadonlyEntry(self, text="bps換算", width=9)
        mon_bps.Entry.configure(textvariable=TxController.MonitorParams().bps)

        # 送信元ポート
        mon_srcport = Common.LabelReadonlyEntry(self, text="送信元ポート", width=6)
        mon_srcport.Entry.configure(
            textvariable=TxController.MonitorParams().srcport)

        # 表示設定
        mon_pps.grid(row=0, column=0)
        mon_datalen.grid(row=0, column=1)
        mon_bps.grid(row=0, column=2)
        mon_srcport.grid(row=1, column=0)


class ControllerField(ttk.Frame):
    """ コントローラフィールド """

    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        # 送信ボタン
        button = ttk.Button(self, text="送信開始")
        button.configure(textvariable=TxController.MonitorParams().send_btn)
        button.configure(command=TxController.SendAction(widgets=txWidgets))
        button.pack(side=tk.LEFT, ipady=5)

# =================================
# == 表示メイン処理
# =================================


def show(master):
    SettingField(master).grid(row=0, column=0, rowspan=2)
    MonitorField(master).grid(row=0, column=1)
    ControllerField(master).grid(row=1, column=1)
