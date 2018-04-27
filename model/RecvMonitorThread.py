# -*- coding: utf-8 -*-

import threading
import time


class RecvMonitorThread(threading.Thread):
    def __init__(self, share_obj, datalen, pps):
        super(RecvMonitorThread, self).__init__()
        self.share_obj = share_obj
        self.datalen = datalen
        self.pps = pps
        self.stop_flg = False

    def run(self):
        while True:
            time.sleep(1)
            self._update()
            if self.stop_flg:
                break
        self._clear()

    def stop(self):
        self.stop_flg = True

    def _update(self):
        tmp_count = self.share_obj.count
        tmp_total = self.share_obj.total
        self.share_obj.count = 0
        self.share_obj.total = 0
        self.pps.set(tmp_count)
        if tmp_count > 0 and tmp_total > 0:
            self.datalen.set(int(tmp_total/tmp_count))
        else:
            self.datalen.set(0)

    def _clear(self):
        self.pps.set(0)
        self.share_obj.count = 0
