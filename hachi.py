# -*- coding: utf-8 -*-

import os
import tkinter as tk
from tkinter import ttk

from view import RxField, TxField, LogField, MenuBar


class App():
    def __init__(self, master):

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
        main_frame = ttk.Frame(master)
        main_frame.pack()

        RxField.RxField(main_frame)
        TxField.TxField(main_frame)
        LogField.LogField(main_frame)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("hachi")
    app = App(root)
    root.mainloop()
