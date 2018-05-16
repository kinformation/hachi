# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk

from model import HachiUtil
from view import Common
from controller import TxController


class TxParams:
    """ パケット送信パラメータクラス """

    def __init__(self):
        self.__proto = tk.IntVar(value=1)
        self.__host = tk.StringVar(value="169.254.1.80")
        self.__dstport_st = tk.IntVar(value=12000)
        self.__dstport_ed = tk.IntVar(value=12002)
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
    """送信領域表示設定クラス"""

    def __init__(self, master):
        # 各種パラメータ格納クラス
        self.txParams = TxParams()
        # パケット送信中に非活性するウィジェットを格納(辞書型)
        self.txWidgets = {}
        # 送信領域描画
        self._tx_field(master)

    def _tx_field(self, master):
        """ 送信フィールド表示設定 """

        # 送信設定(左側)
        left_frame = ttk.LabelFrame(master, text="送信設定")
        left_frame.grid(row=1, column=0, sticky=tk.NW+tk.E)
        self._left_field(left_frame)

        # モニタ、コントローラ(右側)
        right_frame = ttk.Frame(master)
        right_frame.grid(row=1, column=1, sticky=tk.NW)
        self._right_field(right_frame)

    # ============= レイヤー1 =============

    def _left_field(self, master):
        """ 送信フィールド左側表示設定 """

        # 使用プロトコル(1列目)
        frame_proto = ttk.Frame(master)
        frame_proto.pack(anchor=tk.NW)
        self._proto_field(frame_proto)

        # 送信先設定(2列目)
        frame_dst = ttk.Frame(master)
        frame_dst.pack(anchor=tk.NW)
        self._dst_addr_field(frame_dst)

        # 送信元設定(3列目)
        frame_src = ttk.Frame(master)
        frame_src.pack(anchor=tk.NW)
        self._dst_addr_field(frame_src)

        # 送信パラメータ設定(4列目)
        frame_param = ttk.Frame(master)
        frame_param.pack(anchor=tk.NW)
        self._set_param_field(frame_param)

    def _right_field(self, master):
        """ 送信フィールド右側表示設定 """

        # 送信モニター(1列目)
        frame_monitor = ttk.Frame(master)
        frame_monitor.pack(anchor=tk.NW)
        self._monitor_field(frame_monitor)

        # コントローラ(2列目)
        frame_controller = ttk.Frame(master)
        frame_controller.pack(anchor=tk.NW)
        self._controller_field(frame_controller)

    # ============= レイヤー2 =============

    def _proto_field(self, master):
        """ 使用プロトコル表示設定 """

        frame = ttk.LabelFrame(master, text="使用プロトコル")
        frame.pack(side=tk.LEFT)

        # プロトコルリスト
        radio_item = {
            'radio_tcp': {'text': "TCP", 'value': 0},
            'radio_udp': {'text': "UDP", 'value': 1},
            # originalは使わなさそうなので除外
            # 'radio_org': {'text': "Original", 'value': 2},
        }

        for key, val in radio_item.items():
            item = ttk.Radiobutton(
                frame, text=val['text'], value=val['value'], variable=self.txParams.proto)
            item.pack(side=tk.LEFT)
            self.txWidgets[key] = item

    def _dst_addr_field(self, parent_frame):
        """ 送信先設定表示設定 """

        frame = ttk.LabelFrame(parent_frame, text="送信先設定")
        frame.pack()

        entry_host = Common.LabelEntry(
            frame, text="IPアドレス", width=30, textvariable=self.txParams.host)
        entry_host.pack(side=tk.LEFT, anchor=tk.N)
        self.txWidgets["entry_host"] = entry_host.Entry

        # ポート設定
        self._set_port_field(frame)

        entry_host = Common.LabelEntry(
            frame, text="IPアドレス", width=30, textvariable=self.txParams.host)
        entry_host.pack(side=tk.LEFT, anchor=tk.N)
        self.txWidgets["entry_host"] = entry_host.Entry

        # ポート設定
        self._set_port_field(frame)

    # ===== 送信先ポート設定 =====
    def _set_port_field(self, parent_frame):

        frame = ttk.Frame(parent_frame)
        frame.pack(side=tk.LEFT)

        # ===== 宛先ポート入力 =====
        frame_port = ttk.Frame(frame)
        frame_port.pack(side=tk.LEFT)

        # Label("ポート")
        ttk.Label(frame_port, text="ポート").pack(side=tk.LEFT)

        # Entry(範囲指定：開始)
        entry_port_st = ttk.Entry(
            frame_port, width=6, textvariable=self.txParams.dstport_st)
        entry_port_st.pack(side=tk.LEFT)
        # Label("～")
        ttk.Label(frame_port, text="～").pack(side=tk.LEFT)
        # Entry(範囲指定：終了)
        entry_port_ed = ttk.Entry(
            frame_port, width=6, textvariable=self.txParams.dstport_ed)
        entry_port_ed.pack(side=tk.LEFT)
        # ===== 宛先ポート入力:終わり =====

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
        combo_porttype.pack(anchor=tk.E)
        # ===== ポート指定種別(プルダウン):終わり =====

        # ===== プロトコルがUDPの時だけポート指定種別選択を有効化 =====
        # アクションクラス
        porttype_udponly = HachiUtil.ChangeSendProto(
            self.txParams.proto, combo_porttype, self.txParams.dstport_type)
        # ラジオボタンの値更新時に発火するよう登録
        self.txParams.proto.trace("w", porttype_udponly)
        # 初回実行
        porttype_udponly()
        # ===== プロトコルがUDPの時だけポート指定種別選択を有効化:終わり =====

        self.txWidgets["entry_port_st"] = entry_port_st
        self.txWidgets["entry_port_ed"] = entry_port_ed
        self.txWidgets["combo_porttype"] = combo_porttype

    def _set_param_field(self, master):
        """ 送信パラメータ設定表示設定 """

        # データ長
        entry_datalen = Common.LabelEntry(
            master, text="データ長", width=6, textvariable=self.txParams.datalen)
        entry_datalen.pack(side=tk.LEFT)

        # 送信パケット数/秒
        entry_pps = Common.LabelEntry(
            master, text="送信パケット数/秒", width=6, textvariable=self.txParams.pps)
        entry_pps.pack(side=tk.LEFT)

        # 最高速
        check_unlimited = HachiUtil.CheckUnlimited(
            self.txParams.unlimited, entry_pps.Entry)
        chbtn_unlimited = ttk.Checkbutton(
            master, text='最高速', variable=self.txParams.unlimited, command=check_unlimited)
        chbtn_unlimited.pack(side=tk.LEFT)

        # 送信速度の目安
        ttk.Label(master, text="送信速度の目安:   ").pack(side=tk.LEFT)
        ttk.Label(master, textvariable=self.txParams.predicted_bps).pack(
            side=tk.LEFT)

        self.txWidgets["entry_datalen"] = entry_datalen.Entry
        self.txWidgets["entry_pps"] = entry_pps.Entry
        self.txWidgets["chbtn_unlimited"] = chbtn_unlimited

    def _monitor_field(self, master):
        """ 送信モニター表示設定 """

        frame = ttk.LabelFrame(master, text="送信モニター")
        frame.pack()

        # 送信数/秒
        Common.LabelReadonlyEntry(frame, text="送信数/秒", width=7,
                                  textvariable=self.txParams.real_pps).grid(row=0, column=0)

        # データ長(Byte)
        Common.LabelReadonlyEntry(frame, text="データ長(Byte)", width=6,
                                  textvariable=self.txParams.datalen).grid(row=0, column=1)

        # bps換算
        Common.LabelReadonlyEntry(frame, text="bps換算", width=9,
                                  textvariable=self.txParams.real_bps).grid(row=0, column=2)

        # 送信元ポート
        Common.LabelReadonlyEntry(frame, text="送信元ポート", width=6, textvariable=self.txParams.srcport).grid(
            row=1, column=0, columnspan=3, sticky=tk.W)

    def _controller_field(self, parent_frame):
        """ コントローラ(送信ボタン)表示設定 """

        sendAction = TxController.SendAction(self.txParams, self.txWidgets)
        button = ttk.Button(
            parent_frame, textvariable=self.txParams.send_btn_text, command=sendAction)
        button.pack(side=tk.LEFT, ipady=5)
