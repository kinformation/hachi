# -*- coding: utf-8 -*-
import sys
import threading
import time


class SendMonitorThread(threading.Thread):
    def __init__(self, sendcount, realpps):
        super(SendMonitorThread, self).__init__()
        self.sendcount = sendcount
        self.realpps = realpps
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
        self.realpps.set(0)
        self.sendcount.num = 0

    def _update(self):
        self.current = self.sendcount.num
        self.realpps.set(self.current - self.prev)
        self.prev = self.current

        # オーバーフロー対策
        # int最大値の半分以上でリセット
        if self.current > sys.maxsize / 2:
            self._reset()

    def _reset(self):
        self.current = 0
        self.prev = 0
        self.sendcount.num = 0
