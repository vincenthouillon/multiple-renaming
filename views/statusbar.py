#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# pylint: disable=undefined-variable
# flake8: noqa: F821

"""Called from views.view"""

import sys
from tkinter import IntVar, StringVar, ttk


class StatusBar:
    """ Display a satusbar. """

    def __init__(self, parent):
        self.parent = parent

        self.var_alert = StringVar()
        self.var_nbfiles = IntVar()

        self.set_ui()

    def set_ui(self):
        """Make widget statusbar."""
        frm_status = ttk.Frame(self.parent, relief="sunken")
        frm_status.pack(fill="x")

        row_status = ttk.Frame(frm_status)
        row_status.pack(fill="x")

        lbl_count_files = ttk.Label(
            row_status, textvariable=self.var_nbfiles)
        lbl_count_files.pack(side="left")

        lbl_files = ttk.Label(
            row_status, text=_("file(s)") + " | ")
        lbl_files.pack(side="left")

        if sys.platform == "darwin":
            lbl_alert = ttk.Label(
                row_status,
                textvariable=self.var_alert,
                foreground="red",
                font=("sans-serif", 12, "bold"))
        else:
            lbl_alert = ttk.Label(
                row_status,
                textvariable=self.var_alert,
                foreground="red",
                font=("sans-serif", 9, "bold"))

        lbl_alert.pack(side="left")
