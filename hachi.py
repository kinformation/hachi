# -*- coding: utf-8 -*-

import os
import sys
import tkinter as tk
from tkinter import ttk

from view import RxField, TxField, LogField, MenuBar


class App():
    def __init__(self, master):
        # ===== ウィンドウ基本設定 =====
        # タイトル
        master.title("hachi")
        # フォント
        master.option_add('*font', '"Meiryo UI" 9')
        # ウィンドウサイズ変更禁止
        master.resizable(0, 0)
        # アイコン
        icon = self.resource_path('hachi.ico')
        master.iconbitmap(icon)

        # ===== メニューバー =====
        menubar = tk.Menu(master)
        master.configure(menu=menubar)
        MenuBar.MenuBar(menubar)

        # ===== メインフレーム =====
        RxField.show(master)
        TxField.show(master)
        LogField.show(master)

    def resource_path(self, relative):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative)
        return os.path.join(relative)


import ctypes


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if __name__ == '__main__':
    if is_admin():
        master = tk.Tk()
        App(master)
        master.mainloop()
    else:
        print(sys.executable)
        print(__file__)
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, __file__, None,  0)

    # master = tk.Tk()
    # App(master)
    # master.mainloop()
