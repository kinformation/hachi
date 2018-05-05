# -*- coding: utf-8 -*-

"""
TCPでパケットを投げるスレッド
"""

import socket
import time
from itertools import repeat
from contextlib import closing
from tkinter import messagebox

from model import SendThread
from controller import TxController


class SendTcpThread(SendThread.SendThread):
    def __init__(self, params, counter):
        super().__init__(params, counter)

        # TCP送信用ソケット生成
        self.sock = socket.socket(self.family, socket.SOCK_STREAM)
        # コネクションタイムアウト値設定：3秒
        self.sock.settimeout(3.0)

    def run(self):

        try:
            # TCPコネクション生成
            self.sock.connect(self.address)
            # 送信元ポート通知
            self.srcport_obj.set(self.sock.getsockname()[1])

            # 最高速の処理を軽くするため処理を分ける
            if self.unlimited:
                self._send_u()
            else:
                self._send()
        except Exception as e:
            TxController.tcp_exception(e)
        finally:
            self.sock.close()

    def _send(self):
        # whileはforより圧倒的にループが遅い
        st = 0
        for _ in repeat(0):
            st = time.perf_counter()
            self.sock.send(self.payload)
            self.counter.num += 1
            if self.stop_flg:
                break

            # タイマー
            while time.perf_counter() - st < self.freq:
                pass

    def _send_u(self):
        for _ in repeat(0):
            self.sock.send(self.payload)
            self.counter.num += 1
            if self.stop_flg:
                break
