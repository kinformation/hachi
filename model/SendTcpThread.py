# -*- coding: utf-8 -*-

import socket
import time
from itertools import repeat

from model import SendThread
from controller import TxController


class SendTcpThread(SendThread.SendThread):
    """ TCPパケットを投げるスレッド """

    def __init__(self, params, sendObj, srcport):
        super().__init__(params, sendObj, srcport)

        # memo: 現状、複数送信元、複数送信先設定なし

        # TCP送信用ソケット生成
        self.sock = socket.socket(self.family, socket.SOCK_STREAM)
        # 送信元ポート設定
        self.sock.bind((self.ZERO_IP, self.srcaddr_list[0][1]))
        # コネクションタイムアウト値設定：3秒
        self.sock.settimeout(3.0)

    def run(self):

        try:
            # TCPコネクション生成
            self.sock.connect(self.dstaddr_list[0])
            # # 送信元ポート通知
            # self.srcport.set(self.sock.getsockname()[1])

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
            self.sock.send(self.data)
            self.sendObj.count += 1
            if self.stop_flg:
                break

            # タイマー
            while time.perf_counter() - st < self.freq:
                pass

    def _send_u(self):
        for _ in repeat(0):
            self.sock.send(self.data)
            self.sendObj.count += 1
            if self.stop_flg:
                break
