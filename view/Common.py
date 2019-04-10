# -*- coding: utf-8 -*-

import sys
import os

import tkinter as tk
from tkinter import ttk

# =================================
# == 公開関数
# =================================


def resource_path(relative):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)

# =================================
# == 公開クラス
# =================================


class LabelEntry(ttk.Frame):
    """ ラベル付きEntry（横並び） """

    def __init__(self, master=None, text=None, **entry_kw):
        ttk.Frame.__init__(self, master)
        # Label
        self.Label = ttk.Label(self, text=text)
        self.Label.pack(side=tk.LEFT)
        # Entry
        self.Entry = ttk.Entry(self)
        self.Entry.configure(entry_kw)
        self.Entry.pack()


class LabelReadonlyEntry(ttk.Frame):
    """ ラベル付き非活性Entry（縦並び） """

    def __init__(self, master=None, text=None, **entry_kw):
        ttk.Frame.__init__(self, master)
        # Label
        self.Label = ttk.Label(self, text=text)
        self.Label.pack()
        # Entry
        self.Entry = ttk.Entry(self, justify=tk.RIGHT)
        self.Entry.configure(entry_kw)
        self.Entry.state(['readonly'])
        self.Entry.pack()
