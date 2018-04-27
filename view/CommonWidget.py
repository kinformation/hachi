# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk

# ラジオボタン


def set_radio(parent_frame, text, value, textvariable):
    radio = ttk.Radiobutton(parent_frame, text=text, value=value,
                            variable=textvariable)
    radio.pack(side=tk.LEFT)
    return radio

# ラベル付きEntry（横並び）


def set_label_entry(parent_frame, labeltext, width, textvariable, side=tk.LEFT):
    frame = ttk.Frame(parent_frame)
    frame.pack(side=side)

    # Label
    ttk.Label(frame, text=labeltext).pack(side=tk.LEFT)
    # Entry
    entry = ttk.Entry(frame, width=width, textvariable=textvariable)
    entry.pack(side=tk.LEFT)

    return entry

# ラベル付き非活性Entry（縦並び）


def set_label_disable_entry(parent_frame, labeltext, width, textvariable):
    frame = ttk.Frame(parent_frame)
    frame.pack(side=tk.LEFT)

    # Label
    ttk.Label(frame, text=labeltext).pack()
    # Entry
    entry = ttk.Entry(frame, width=width,
                      textvariable=textvariable, justify=tk.RIGHT)
    entry.state(['readonly'])
    entry.pack()

    return entry
