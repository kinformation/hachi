# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk

from controller import LogController


class LogField:
    """ 表示領域の設定 """

    def __init__(self):
        pass

    def set_log_field(self, parent_frame):

        frame = ttk.Frame(parent_frame)
        frame.pack()

        # ログ表示エリア
        log_area = tk.Text(frame, height=8)
        log_area.pack(fill=tk.BOTH, side=tk.LEFT)
        logger = LogController.LogController(log_area)
        logger.insert("hachiが起動しました")

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            frame, orient=tk.VERTICAL, command=log_area.yview)
        log_area['yscrollcommand'] = scrollbar.set
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
