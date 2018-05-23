# -*- coding: utf-8 -*-
import sys
import tkinter as tk

from controller import MenuController


class MenuBar:
    """ メニューバー領域 """

    def __init__(self, master):
        # ファイル(F)
        menu_file = tk.Menu(master, tearoff=False)
        master.add_cascade(label="ファイル(F)", underline=5, menu=menu_file)
        self._file_menu(menu_file)

        # オプション
        menu_option = tk.Menu(master, tearoff=False)
        master.add_cascade(label="オプション", menu=menu_option)
        self._option_menu(menu_option)

        # ヘルプ(H)
        menu_help = tk.Menu(master, tearoff=False)
        master.add_cascade(label="ヘルプ(H)", underline=4, menu=menu_help)
        self._help_menu(menu_help)

    def _file_menu(self, menu):
        """ ファイル(F) サブメニュー """

        # ログの保存
        menu.add_command(
            label="ログの保存", command=MenuController.SaveLog())

        # 管理者モードで実行(生パケット生成が必要になったときに復活させる)
        # menu.add_command(
        #     label="管理者モードで実行", command=MenuController.AdvancedExec())

        # 終了
        menu.add_command(label="終了", command=sys.exit)

    def _option_menu(self, menu):
        """ オプション サブメニュー """

        # タスク優先度
        tgl = tk.IntVar(value=1)
        submenu_task_priority = tk.Menu(menu, tearoff=False)
        menu.add_cascade(label="タスク優先度", menu=submenu_task_priority)
        for n, item in enumerate(("高", "通常", "低")):
            submenu_task_priority.add_radiobutton(
                label=item, variable=tgl, value=n, command=MenuController.TaskPriority(tgl))

        # 送信データ長ランダム
        # menu.add_command(label="ランダムデータ長送信")

        # 送信パケット数ランダム
        # menu.add_command(label="ランダムパケット数送信")

        # インターフェース更新
        # menu.add_command(label="インターフェース更新")

    def _help_menu(self, menu):
        """ ヘルプ(H) サブメニュー """

        # バージョン情報(A)
        menu.add_command(label="バージョン情報(A)", under=8,
                         command=MenuController.ShowVersion())
