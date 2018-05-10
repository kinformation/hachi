# -*- coding: utf-8 -*-

import os
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
        icon = "{}/hachi.ico".format(os.path.dirname(
            os.path.abspath(__file__)))
        master.iconbitmap(icon)

        # ===== メニューバー =====
        menubar = tk.Menu(master)
        master.configure(menu=menubar)
        MenuBar.MenuBar(menubar)

        # ===== メインフレーム =====
        RxField.RxField(master)
        TxField.TxField(master)
        LogField.LogField(master)


if __name__ == '__main__':
    master = tk.Tk()
    App(master)
    master.mainloop()
