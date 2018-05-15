# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk


class LabelEntry(ttk.Frame):
    """ ラベル付きEntry（横並び） """

    def __init__(self, master=None, text=None, width=None, textvariable=None):
        ttk.Frame.__init__(self, master)
        # Label
        self.Label = ttk.Label(self, text=text)
        self.Label.pack(side=tk.LEFT)
        # Entry
        self.Entry = ttk.Entry(self, width=width, textvariable=textvariable)
        self.Entry.pack()


class LabelReadonlyEntry(ttk.Frame):
    """ ラベル付き非活性Entry（縦並び） """

    def __init__(self, master=None, text=None, width=None, textvariable=None):
        ttk.Frame.__init__(self, master)
        # Label
        self.Label = ttk.Label(self, text=text)
        self.Label.pack()
        # Entry
        self.Entry = ttk.Entry(self, width=width,
                               textvariable=textvariable, justify=tk.RIGHT)
        self.Entry.state(['readonly'])
        self.Entry.pack()
