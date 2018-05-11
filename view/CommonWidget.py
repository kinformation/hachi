# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk


class LabelEntry(ttk.Frame):
    # ラベル付きEntry（横並び）
    def __init__(self, master=None, text=None, width=None, textvariable=None):
        ttk.Frame.__init__(self, master)
        # Label
        ttk.Label(self, text=text).pack(side=tk.LEFT)
        # Entry
        ttk.Entry(self, width=width, textvariable=textvariable).pack()


class LabelReadonlyEntry(ttk.Frame):
    # ラベル付き非活性Entry（縦並び）
    def __init__(self, master=None, text=None, width=None, textvariable=None):
        ttk.Frame.__init__(self, master)
        # Label
        ttk.Label(self, text=text).pack()
        # Entry
        entry = ttk.Entry(self, width=width,
                          textvariable=textvariable, justify=tk.RIGHT)
        entry.state(['readonly'])
        entry.pack()
