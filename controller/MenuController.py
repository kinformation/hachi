# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox, filedialog
import sys
import ctypes
import time

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


class AdvancedExec:
    """ 管理者権限で実行 """

    def __init__(self):
        pass

    def __call__(self):
        opt = __file__ + "\\..\\..\\hachi.py"
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, opt, None,  1)

        # すぐ終了させると起動失敗するから少し待つ
        time.sleep(1)
        sys.exit()


class TaskPriority:
    def __init__(self, priority):
        self.priority = priority

    def __call__(self):
        self._setpriority(priority=self.priority.get())

    def _setpriority(self, pid=None, priority=1):
        import win32api
        import win32process
        import win32con

        priorityclasses = [win32process.HIGH_PRIORITY_CLASS,
                           win32process.NORMAL_PRIORITY_CLASS,
                           win32process.IDLE_PRIORITY_CLASS]
        if pid == None:
            pid = win32api.GetCurrentProcessId()
        handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
        win32process.SetPriorityClass(handle, priorityclasses[priority])
