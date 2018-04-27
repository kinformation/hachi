# -*- coding: utf-8 -*-
import sys
import tkinter as tk

from controller import MenuController


"""
メニューバー領域
"""


class MenuBar:
    def __init__(self, master):
        self._set_menubar(master)

    def _set_menubar(self, parent_menu):
        # ファイル(F)
        self._set_file_menu(parent_menu)
        # オプション
        self._set_option_menu(parent_menu)
        # ヘルプ(H)
        self._set_help_menu(parent_menu)

    def _set_file_menu(self, parent_menu):
        menu_file = tk.Menu(parent_menu, tearoff=False)
        parent_menu.add_cascade(label="ファイル(F)", underline=5, menu=menu_file)

        # 項目
        menu_file.add_command(
            label="ログの保存", command=MenuController.SaveLog())
        menu_file.add_command(label="終了(X)", under=3, command=sys.exit)

    def _set_option_menu(self, parent_menu):
        menu_option = tk.Menu(parent_menu, tearoff=False)
        parent_menu.add_cascade(label="オプション", menu=menu_option)

        # 項目(未定)

    def _set_help_menu(self, parent_menu):
        menu_help = tk.Menu(parent_menu, tearoff=False)
        parent_menu.add_cascade(label="ヘルプ(H)", underline=4, menu=menu_help)

        # 項目
        menu_help.add_command(label="バージョン情報(A)", under=8,
                              command=MenuController.ShowVersion())
