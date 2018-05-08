# -*- coding: utf-8 -*-
import tkinter as tk
from datetime import datetime


class LogController:
    _instance = None

    def __new__(cls, log_area=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.log_area = log_area
            cls.insert(cls, "hachiが起動しました")

        return cls._instance

    def __init__(self, log_area=None):
        pass

    def insert(self, msg):
        # 書き込み禁止解除:ログ挿入するために必要
        self.log_area['state'] = tk.NORMAL

        timestamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        self.log_area.insert(tk.END, "[{}] {}\n".format(timestamp, msg))
        # 最終行へスクロール
        self.log_area.see(tk.END)

        # 書き込み禁止設定
        self.log_area['state'] = tk.DISABLED

    def get(self):
        return self.log_area.get('1.0', tk.END)
