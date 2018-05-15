# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import scrolledtext

from controller import LogController


class LogField:
    """ ログ表示領域の設定 """

    def __init__(self, master):
        self._set_log_field(master)

    def _set_log_field(self, parent_frame):
        log_area = scrolledtext.ScrolledText(parent_frame, height=8)
        log_area.grid(row=2, column=0, columnspan=2, sticky=tk.W+tk.E)
        # ここでLogControllerを最初に呼ぶこと
        LogController.LogController(log_area)
