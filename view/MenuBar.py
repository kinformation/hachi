# -*- coding: utf-8 -*-
import sys
import tkinter as tk

from controller import MenuController


"""
メニューバー領域
"""


class MenuBar:
    def __init__(self, master):
        # ファイル(F)
        self._file_menu(master)
        # オプション
        self._option_menu(master)
        # ヘルプ(H)
        self._help_menu(master)

    def _file_menu(self, parent_menu):
        menu_file = tk.Menu(parent_menu, tearoff=False)
        parent_menu.add_cascade(label="ファイル(F)", underline=5, menu=menu_file)

        # 項目
        menu_file.add_command(
            label="ログの保存", command=MenuController.SaveLog())
        menu_file.add_command(label="終了(X)", under=3, command=sys.exit)

    def _option_menu(self, parent_menu):
        menu_option = tk.Menu(parent_menu, tearoff=False)
        parent_menu.add_cascade(label="オプション", menu=menu_option)

        # タスク優先度
        tgl = tk.IntVar(value=1)
        submenu_task_priority = tk.Menu(parent_menu, tearoff=False)
        menu_option.add_cascade(label="タスク優先度", menu=submenu_task_priority)
        for n, item in enumerate(("高", "通常", "低")):
            submenu_task_priority.add_radiobutton(
                label=item, variable=tgl, value=n, command=MenuController.TaskPriority(tgl))

        # 送信データ長ランダム
        # menu_option.add_command(label="ランダムデータ長送信")

        # 送信パケット数ランダム
        # menu_option.add_command(label="ランダムパケット数送信")

        # インターフェース更新
        # menu_option.add_command(label="インターフェース更新")

    def _help_menu(self, parent_menu):
        menu_help = tk.Menu(parent_menu, tearoff=False)
        parent_menu.add_cascade(label="ヘルプ(H)", underline=4, menu=menu_help)

        # 項目
        menu_help.add_command(label="バージョン情報(A)", under=8,
                              command=MenuController.ShowVersion())
