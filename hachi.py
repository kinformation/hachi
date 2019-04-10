# -*- coding: utf-8 -*-

import os
import sys
import tkinter as tk
from tkinter import ttk

from view import RxField, TxField, LogField, MenuBar, Common


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
        icon = Common.resource_path('hachi.ico')
        master.iconbitmap(icon)

        # ===== メニューバー =====
        menubar = tk.Menu(master)
        master.configure(menu=menubar)
        MenuBar.MenuBar(menubar)

        # ===== メインフレーム =====
        RxField.show(master)
        TxField.show(master)
        LogField.show(master)


if __name__ == '__main__':
    master = tk.Tk()
    App(master)
    master.mainloop()
