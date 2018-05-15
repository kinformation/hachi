# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk

from model import HachiUtil
from view import Common
from controller import RxController


class RxParams:
    """ パケット受信パラメータクラス """

    def __init__(self):
        self.__proto = tk.IntVar(value=1)
        self.__host = tk.StringVar()
        self.__port = tk.IntVar(value=12000)
        self.__real_datalen = tk.IntVar(value=0)
        self.__real_bps = tk.StringVar(value="0 bps")
        self.__real_pps = tk.IntVar(value=0)
        self.__recv_btn_text = tk.StringVar(value="受信開始")

        updateBps = HachiUtil.UpdateBps(
            self.__real_datalen, self.__real_pps, self.__real_bps)
        # 値更新時に発火するよう登録
        self.__real_pps.trace("w", updateBps)

    @property
    def proto(self):
        return self.__proto

    @property
    def host(self):
        return self.__host

    @property
    def port(self):
        return self.__port

    @property
    def real_datalen(self):
        return self.__real_datalen

    @property
    def real_bps(self):
        return self.__real_bps

    @property
    def real_pps(self):
        return self.__real_pps

    @property
    def recv_btn_text(self):
        return self.__recv_btn_text


class RxField:
    """ 表示領域の設定 """

    def __init__(self, master):
        # 各種パラメータ格納クラス
        self.rxParams = RxParams()
        # パケット送信中に非活性するウィジェットを格納(辞書型)
        self.rxWidgets = {}
        # 受信フィールド描画開始
        self._set_rx_field(master)

    # ===== 受信フィールド =====
    def _set_rx_field(self, parent_frame):
        # 左ペイン(受信設定)
        left_frame = ttk.LabelFrame(parent_frame, text="受信設定")
        left_frame.grid(row=0, column=0, sticky=tk.NW+tk.E)
        self._set_left_field(left_frame)

        # 右ペイン(モニタ、コントローラ)
        right_frame = ttk.Frame(parent_frame)
        right_frame.grid(row=0, column=1, sticky=tk.NW)
        self._set_right_field(right_frame)

    # ===== 受信フィールド:左ペイン =====
    def _set_left_field(self, parent_frame):
        # 左上ペイン(プロトコル、Multicast)
        frame0 = ttk.Frame(parent_frame)
        frame0.pack(anchor=tk.W)
        self._set_proto_field(frame0)
        # ※Multicast使わなさそうなのでコメントアウト
        # self._set_multicast_field(frame0)

        # 左下ペイン(待ち受けアドレス、ポート設定)
        frame1 = ttk.Frame(parent_frame)
        frame1.pack(fill=tk.X)
        self._set_addr_field(frame1)

    # ===== 受信フィールド:右ペイン =====
    def _set_right_field(self, parent_frame):
        # 右上ペイン
        frame0 = ttk.Frame(parent_frame)
        frame0.pack()
        self._set_monitor_field(frame0)

        # 右下ペイン
        frame1 = ttk.Frame(parent_frame)
        frame1.pack(fill=tk.BOTH)
        self._set_controller_field(frame1)

    # ===== 使用プロトコル =====
    def _set_proto_field(self, parent_frame):
        frame = ttk.LabelFrame(parent_frame, text="使用プロトコル")
        frame.pack(side=tk.LEFT)

        radio_tcp = ttk.Radiobutton(
            frame, text="TCP", value=0, variable=self.rxParams.proto)
        radio_udp = ttk.Radiobutton(
            frame, text="UDP", value=1, variable=self.rxParams.proto)

        radio_tcp.pack(side=tk.LEFT)
        radio_udp.pack(side=tk.LEFT)

        self.rxWidgets["radio_tcp"] = radio_tcp
        self.rxWidgets["radio_udp"] = radio_udp

    # ===== Multicast(未使用) =====
    def _set_multicast_field(self, parent_frame):
        frame = ttk.LabelFrame(parent_frame, text="Multicast")
        frame.pack(fill=tk.BOTH)

        ttk.Checkbutton(frame, text='Use').pack(side=tk.LEFT)
        ttk.Entry(frame, width=16).pack(side=tk.LEFT)

    # ===== 受信ポート設定 =====
    def _set_addr_field(self, parent_frame):
        frame = ttk.LabelFrame(parent_frame, text="受信ポート設定")
        frame.pack(fill=tk.X)

        ttk.Label(frame, text="IPアドレス").pack(side=tk.LEFT)
        address_list = (HachiUtil.LocalAddress())()
        combo_host = ttk.Combobox(
            frame, width=28, values=address_list, textvariable=self.rxParams.host)
        self.rxParams.host.set(address_list[0])
        # IPアドレスをコピーできるようにするため、ROにしない
        # combo_host.state(['readonly'])
        combo_host.pack(side=tk.LEFT)

        entry_port = Common.LabelEntry(
            frame, text="ポート", width=6, textvariable=self.rxParams.port)
        entry_port.pack(side=tk.LEFT)

        self.rxWidgets["combo_host"] = combo_host
        self.rxWidgets["entry_port"] = entry_port

    # ===== 受信モニター =====
    def _set_monitor_field(self, parent_frame):
        frame = ttk.LabelFrame(parent_frame, text="受信モニター")
        frame.pack()

        Common.LabelReadonlyEntry(
            frame, text="受信数/秒", width=7, textvariable=self.rxParams.real_pps).pack(side=tk.LEFT)
        Common.LabelReadonlyEntry(
            frame, text="データ長(Byte)", width=6, textvariable=self.rxParams.real_datalen).pack(side=tk.LEFT)
        Common.LabelReadonlyEntry(
            frame, text="bps換算", width=9, textvariable=self.rxParams.real_bps).pack(side=tk.LEFT)

    # ===== 受信ボタン =====
    def _set_controller_field(self, parent_frame):
        recvAction = RxController.RecvAction(self.rxParams, self.rxWidgets)
        button = ttk.Button(
            parent_frame, textvariable=self.rxParams.recv_btn_text, command=recvAction)
        button.pack(side=tk.LEFT, ipady=10)
        # 必要なら復活させる
        # ttk.Checkbutton(parent_frame, text='ログ').pack(side=tk.LEFT)
