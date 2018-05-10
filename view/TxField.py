# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk

from model import HachiUtil
from view import CommonWidget
from controller import TxController


class TxParams:
    """
    パケット送信パラメータクラス
    """

    def __init__(self):
        self.__proto = tk.IntVar(value=1)
        self.__host = tk.StringVar(value="169.254.1.80")
        self.__dstport_st = tk.IntVar(value=12000)
        self.__dstport_ed = tk.IntVar(value=12000)
        self.__dstport_type = tk.StringVar()
        self.__datalen = tk.IntVar(value=1024)
        self.__pps = tk.IntVar(value=100)
        self.__unlimited = tk.BooleanVar(False)
        self.__predicted_bps = tk.StringVar()
        self.__real_bps = tk.StringVar()
        self.__real_pps = tk.IntVar(value=0)
        self.__srcport = tk.StringVar()
        self.__send_btn_text = tk.StringVar(value="送信開始")

        updatePredictedBps = HachiUtil.UpdateBps(
            self.__datalen, self.__pps, self.__predicted_bps)
        # 値更新時に発火するよう登録
        self.__datalen.trace("w", updatePredictedBps)
        self.__pps.trace("w", updatePredictedBps)
        # 起動時更新
        updatePredictedBps()

        updateRealBps = HachiUtil.UpdateBps(
            self.__datalen, self.__real_pps, self.__real_bps)
        # 値更新時に発火するよう登録
        self.__real_pps.trace("w", updateRealBps)
        # 起動時更新
        updateRealBps()

    @property
    def proto(self):
        return self.__proto

    @property
    def host(self):
        return self.__host

    @property
    def dstport_st(self):
        return self.__dstport_st

    @property
    def dstport_ed(self):
        return self.__dstport_ed

    @property
    def dstport_type(self):
        return self.__dstport_type

    @property
    def datalen(self):
        return self.__datalen

    @property
    def pps(self):
        return self.__pps

    @property
    def unlimited(self):
        return self.__unlimited

    @property
    def predicted_bps(self):
        return self.__predicted_bps

    @property
    def real_bps(self):
        return self.__real_bps

    @property
    def real_pps(self):
        return self.__real_pps

    @property
    def srcport(self):
        return self.__srcport

    @property
    def send_btn_text(self):
        return self.__send_btn_text


class TxField:
    """送信領域設定クラス"""

    def __init__(self, master):
        # 各種パラメータ格納クラス
        self.txParams = TxParams()
        # パケット送信中に非活性するウィジェットを格納(辞書型)
        self.txWidgets = {}
        # 送信フィールド描画開始
        self._set_tx_field(master)

    # ===== 送信フィールド =====
    def _set_tx_field(self, parent_frame):
        frame = ttk.Frame(parent_frame)
        frame.pack()

        # 左ペイン(送信設定)
        left_frame = ttk.LabelFrame(frame, text="送信設定")
        left_frame.pack(side=tk.LEFT, anchor=tk.NW)
        self._set_left_field(left_frame)

        # 右ペイン(モニタ、コントローラ)
        right_frame = ttk.Frame(frame)
        right_frame.pack(side=tk.LEFT, anchor=tk.NW)
        self._set_right_field(right_frame)

    # ===== 送信フィールド:左ペイン =====
    def _set_left_field(self, parent_frame):
        # 左上ペイン(使用プロトコル)
        frame0 = ttk.Frame(parent_frame)
        frame0.pack(anchor=tk.NW)
        self._set_proto_field(frame0)

        # 左中ペイン(送信先設定)
        frame1 = ttk.Frame(parent_frame)
        frame1.pack(anchor=tk.NW)
        self._set_addr_field(frame1)

        # 左下ペイン(送信パラメタ設定)
        frame2 = ttk.Frame(parent_frame)
        frame2.pack(anchor=tk.NW)
        self._set_param_field(frame2)

    # ===== 送信フィールド:右ペイン =====
    def _set_right_field(self, parent_frame):
        # 右上ペイン(送信モニター)
        frame0 = ttk.Frame(parent_frame)
        frame0.pack(anchor=tk.NW)
        self._set_monitor_field(frame0)

        # 右下ペイン(送信ボタン)
        frame1 = ttk.Frame(parent_frame)
        frame1.pack(fill=tk.BOTH)
        self._set_controller_field(frame1)

    # ===== 使用プロトコル =====
    def _set_proto_field(self, parent_frame):
        frame = ttk.LabelFrame(parent_frame, text="使用プロトコル")
        frame.pack(side=tk.LEFT)

        radio_tcp = CommonWidget.set_radio(
            frame, "TCP", 0, self.txParams.proto)
        radio_udp = CommonWidget.set_radio(
            frame, "UDP", 1, self.txParams.proto)
        # originalは使わなさそうなので、いったん除外
        # radio_org = CommonWidget.set_radio(
        #     frame, "Original", 2, self.txParams.proto)

        self.txWidgets["radio_tcp"] = radio_tcp
        self.txWidgets["radio_udp"] = radio_udp
        # self.txWidgets["radio_org"] = radio_org

    # ===== 送信先設定 =====
    def _set_addr_field(self, parent_frame):
        frame = ttk.LabelFrame(parent_frame, text="送信先設定")
        frame.pack()

        entry_host = CommonWidget.set_label_entry(
            frame, "IPアドレス", 30, self.txParams.host, tk.TOP)
        self.txWidgets["entry_host"] = entry_host

        # ポート設定
        self._set_port_field(frame)

    # ===== 送信先ポート設定 =====
    def _set_port_field(self, parent_frame):

        frame = ttk.Frame(parent_frame)
        frame.pack(side=tk.LEFT)

        # Label("ポート")
        ttk.Label(frame, text="ポート").pack(side=tk.LEFT)

        # Entry(範囲指定：開始)
        entry_port_st = ttk.Entry(
            frame, width=6, textvariable=self.txParams.dstport_st)
        entry_port_st.pack(side=tk.LEFT)
        # Label("～")
        ttk.Label(frame, text="～").pack(side=tk.LEFT)
        # Entry(範囲指定：終了)
        entry_port_ed = ttk.Entry(
            frame, width=6, textvariable=self.txParams.dstport_ed)
        entry_port_ed.pack(side=tk.LEFT)

        # ===== ポート指定種別(プルダウン) =====
        typelist = ('単一', 'ﾗｳﾝﾄﾞﾛﾋﾞﾝ')

        # ウィジェットを渡すため、TxParams.__init__に書けない
        changePortState = HachiUtil.ChangePortState(
            self.txParams.dstport_type, entry_port_ed)
        # プルダウン更新時に発火するよう登録
        self.txParams.dstport_type.trace("w", changePortState)

        combo_porttype = ttk.Combobox(
            frame, width=10, values=typelist, textvariable=self.txParams.dstport_type)
        self.txParams.dstport_type.set(typelist[0])
        combo_porttype.state(['readonly'])
        combo_porttype.pack(side=tk.LEFT)
        # ===== ポート指定種別(プルダウン):終わり =====

        self.txWidgets["entry_port_st"] = entry_port_st
        self.txWidgets["entry_port_ed"] = entry_port_ed
        self.txWidgets["combo_porttype"] = combo_porttype

    # ===== 送信パラメタ設定 =====
    def _set_param_field(self, parent_frame):

        # 上段
        frame0 = ttk.Frame(parent_frame)
        frame0.pack()

        entry_datalen = CommonWidget.set_label_entry(
            frame0, "データ長", 6, self.txParams.datalen)
        entry_pps = CommonWidget.set_label_entry(
            frame0, "送信パケット数/秒", 6, self.txParams.pps)

        check_unlimited = HachiUtil.CheckUnlimited(
            self.txParams.unlimited, entry_pps)
        chbtn_unlimited = ttk.Checkbutton(
            frame0, text='最高速', variable=self.txParams.unlimited, command=check_unlimited)
        chbtn_unlimited.pack(side=tk.LEFT)

        self.txWidgets["entry_datalen"] = entry_datalen
        self.txWidgets["entry_pps"] = entry_pps
        self.txWidgets["chbtn_unlimited"] = chbtn_unlimited

        # 下段
        frame1 = ttk.Frame(parent_frame)
        frame1.pack(anchor=tk.NW)

        ttk.Label(frame1, text="送信速度の目安:       ").pack(side=tk.LEFT)
        ttk.Label(frame1, textvariable=self.txParams.predicted_bps).pack(
            side=tk.LEFT)

    # ===== 送信モニター =====
    def _set_monitor_field(self, parent_frame):
        frame = ttk.LabelFrame(parent_frame, text="送信モニター")
        frame.pack()

        CommonWidget.set_label_disable_entry(
            frame, "送信数/秒", 7, self.txParams.real_pps)
        CommonWidget.set_label_disable_entry(
            frame, "データ長(Byte)", 6, self.txParams.datalen)
        CommonWidget.set_label_disable_entry(
            frame, "bps換算", 9, self.txParams.real_bps)

    # ===== 送信ボタン =====
    def _set_controller_field(self, parent_frame):
        sendAction = TxController.SendAction(self.txParams, self.txWidgets)
        button = ttk.Button(
            parent_frame, textvariable=self.txParams.send_btn_text, command=sendAction)
        button.pack(side=tk.LEFT)

        CommonWidget.set_label_disable_entry(
            parent_frame, "送信元ポート", 6, self.txParams.srcport)
