# -*- coding: utf-8 -*-

import threading
import time


class RecvMonitorThread(threading.Thread):
    """ パケット受信モニタースレッド """

    def __init__(self, params, shareObj):
        super(RecvMonitorThread, self).__init__()
        self.shareObj = shareObj
        self.datalen = params.datalen
        self.pps = params.pps
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
        tmp_count = self.shareObj.count
        tmp_total = self.shareObj.total
        self.shareObj.count = 0
        self.shareObj.total = 0
        self.pps.set(tmp_count)
        if tmp_count > 0 and tmp_total > 0:
            self.datalen.set(int(tmp_total/tmp_count))
        else:
            self.datalen.set(0)

    def _clear(self):
        self.pps.set(0)
        self.shareObj.count = 0
