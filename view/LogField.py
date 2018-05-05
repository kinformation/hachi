# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk

from controller import LogController


class LogField:
    """ 表示領域の設定 """

    def __init__(self, master):
        self._set_log_field(master)

    def _set_log_field(self, parent_frame):

        frame = ttk.Frame(parent_frame)
        frame.pack()

        # ログ表示エリア
        log_area = tk.Text(frame, height=8)
        log_area.pack(fill=tk.BOTH, side=tk.LEFT)
        # ここでLogControllerを最初に呼ぶこと
        LogController.LogController(log_area)

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            frame, orient=tk.VERTICAL, command=log_area.yview)
        log_area['yscrollcommand'] = scrollbar.set
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
