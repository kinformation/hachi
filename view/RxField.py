# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk

from model import HachiUtil
from view import Common
from controller import RxController

# =================================
# == グローバル変数
# =================================
rxWidgets = {}

# =================================
# == 受信領域表示設定
# =================================


class SettingField(ttk.LabelFrame):
    """ 受信設定フィールド """

    def __init__(self, master):
        ttk.LabelFrame.__init__(self, master, text="受信設定")

        # プロトコル設定(1列目)
        ProtocolField(self).pack(anchor=tk.W)
        # 受信先設定(2列目)
        AcceptAddressField(self).pack()


class ProtocolField(ttk.LabelFrame):
    """ 使用プロトコルフィールド """

    def __init__(self, master):
        ttk.LabelFrame.__init__(self, master, text="使用プロトコル")

        # プロトコルリスト
        radio_item = {
            'proto_tcp': {'text': "TCP", 'value': 0},
            'proto_udp': {'text': "UDP", 'value': 1},
        }

        for key, val in radio_item.items():
            item = ttk.Radiobutton(
                self, text=val['text'], value=val['value'])
            item.configure(variable=RxController.RecvParams().proto)
            item.pack(side=tk.LEFT, padx=8)
            rxWidgets[key] = item


class AcceptAddressField(ttk.LabelFrame):
    """ 受信ポート設定フィールド """

    def __init__(self, master):
        ttk.LabelFrame.__init__(self, master, text="受信ポート設定")

        # IPアドレス
        ttk.Label(self, text="IPアドレス").pack(side=tk.LEFT)
        address_list = HachiUtil.LocalAddress().get()
        dstip = ttk.Combobox(self, width=28, values=address_list)
        dstip.configure(textvariable=RxController.RecvParams().ip)
        RxController.RecvParams().ip.set(address_list[0])
        # IPアドレスをコピーできるようにするため、ROにしない
        # combo_host.state(['readonly'])
        dstip.pack(side=tk.LEFT)
        rxWidgets['dstip'] = dstip

        # ポート番号
        dstport = Common.LabelEntry(self, text="ポート番号", width=20)
        dstport.Entry.configure(
            textvariable=RxController.RecvParams().port)
        dstport.pack(anchor=tk.N)
        rxWidgets['dstport'] = dstport.Entry


class MonitorField(ttk.LabelFrame):
    """ 送信モニターフィールド """

    def __init__(self, master):
        ttk.LabelFrame.__init__(self, master, text="受信モニター")

        # 受信数/秒
        mon_pps = Common.LabelReadonlyEntry(self, text="受信数/秒", width=7)
        mon_pps.Entry.configure(textvariable=RxController.MonitorParams().pps)

        # データ長(Byte)
        mon_datalen = Common.LabelReadonlyEntry(
            self, text="データ長(Byte)", width=6)
        mon_datalen.Entry.configure(
            textvariable=RxController.MonitorParams().datalen)

        # bps換算
        mon_bps = Common.LabelReadonlyEntry(self, text="bps換算", width=9)
        mon_bps.Entry.configure(textvariable=RxController.MonitorParams().bps)

        # 表示設定
        mon_pps.grid(row=0, column=0)
        mon_datalen.grid(row=0, column=1)
        mon_bps.grid(row=0, column=2)


class ControllerField(ttk.Frame):
    """ コントローラフィールド """

    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        button = ttk.Button(self)
        button.configure(textvariable=RxController.MonitorParams().recv_btn)
        button.configure(command=RxController.RecvAction(widgets=rxWidgets))
        button.pack(side=tk.LEFT, ipady=5)

        # 必要なら復活させる
        # ttk.Checkbutton(self, text='ログ').pack(side=tk.LEFT)

# =================================
# == 表示メイン処理
# =================================


def show(master):
    SettingField(master).grid(sticky=tk.NW, row=0, column=0, rowspan=2)
    MonitorField(master).grid(sticky=tk.NW, row=0, column=1)
    ControllerField(master).grid(sticky=tk.NW, row=1, column=1)
