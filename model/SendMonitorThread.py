# -*- coding: utf-8 -*-

import sys
import threading
import time


class SendMonitorThread(threading.Thread):
    """ パケット送信モニタースレッド """

    def __init__(self, sendObj, params):
        super(SendMonitorThread, self).__init__()
        self.sendObj = sendObj
        self.pps = params.pps
        self.stop_flg = False
        self.prev = 0
        self.current = 0

    def run(self):
        while True:
            self._update()
            if self.stop_flg:
                break
            # 1秒タイマー
            # ここはtime.perf_counter()つかうと送信精度落ちる
            time.sleep(1)
        self._clear()

    def stop(self):
        self.stop_flg = True

    def _clear(self):
        self.pps.set(0)
        self.sendObj.count = 0

    def _update(self):
        # 頻繁にカウンタリセットすると送信性能落ちるため
        # 差分を拾っていく
        self.current = self.sendObj.count
        self.pps.set(self.current - self.prev)
        self.prev = self.current

        # オーバーフロー対策
        # int最大値の半分以上でリセット
        if self.current > sys.maxsize / 2:
            self._reset()

    def _reset(self):
        self.current = 0
        self.prev = 0
        self.sendObj.count = 0
