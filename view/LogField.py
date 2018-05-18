# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import scrolledtext

from controller import LogController

# =================================
# == ログ表示設定
# =================================


class LogField(scrolledtext.ScrolledText):
    """ ログ表示領域の設定 """

    def __init__(self, master):
        scrolledtext.ScrolledText.__init__(self, master, height=5)
        # ここでLogControllerを最初に呼ぶこと
        LogController.LogController(self)

# =================================
# == 表示処理
# =================================


def show(master):
    LogField(master).grid(row=5, column=0, columnspan=2, sticky=tk.W+tk.E)
