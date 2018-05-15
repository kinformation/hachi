# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox, filedialog

from controller import LogController


class ShowVersion:
    def __init__(self):
        pass

    def __call__(self):
        msg = """
Hachi
Version 1.1.0

Copyright (c) 2018 k.kanatani
"""[1:-1]
        messagebox.showinfo('バージョン情報', msg)


class SaveLog:
    def __init__(self):
        pass

    def __call__(self):
        filename = filedialog.asksaveasfilename(
            initialdir="/", title="ログの保存", filetypes=(("テキスト ファイル", "*.txt"), ("全ての ファイル", "*.*")))
        log = LogController.LogController().get()
        f = open(filename, 'w')
        f.write(log)
        f.close()
