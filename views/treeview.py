#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# pylint: disable=undefined-variable
# flake8: noqa: F821

"""Called from views.view."""

import sys
from tkinter import ttk


class Treeview(ttk.Treeview):
    """ Make treeview widget. """

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.tree_frm = ttk.Frame(self.parent)
        self.tree_frm.pack(fill="both", expand=True)

        columns = (_("Old name"),
                   _("New name"),
                   _("Size"),
                   _("Date modified"),
                   _("Date created"),
                   _("Location")
                   )

        self.style = ttk.Style()

        # Fix background and foreground color display
        self.style.map("Treeview", foreground=self.__fixed_map("foreground"),
                       background=self.__fixed_map("background"))

        # Remove the borders
        if sys.platform == "win32":
            self.style.layout(
                "Treeview", [("Treeview.treearea", {"sticky": "nswe"})])

        self.tree = ttk.Treeview(
            self.tree_frm, show="headings", column=columns, selectmode="none")

        self.tree.tag_configure("ERR", foreground="#d63031")

        # Scrollbars
        horizontal_scrollbar = ttk.Scrollbar(
            self.tree_frm, orient="horizontal", command=self.tree.xview)
        horizontal_scrollbar.pack(side="bottom", fill="x")
        self.tree.configure(xscrollcommand=horizontal_scrollbar.set)

        vertical_scrollbar = ttk.Scrollbar(
            self.tree_frm, orient="vertical", command=self.tree.yview)
        vertical_scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=vertical_scrollbar.set)

        for column in columns:
            self.tree.heading(column, text=column, anchor="w")

        self.tree.column(columns[0], minwidth=180)
        self.tree.column(columns[1], minwidth=180)
        self.tree.column(columns[2], minwidth=40, width=80, anchor="e")
        self.tree.column(columns[3], minwidth=60, width=140)
        self.tree.column(columns[4], minwidth=60, width=140)
        self.tree.column(columns[5], minwidth=60, width=300)

        self.tree.pack(fill="both", expand=True)

    def __fixed_map(self, option):
        # Fix for setting text colour for Tkinter 8.6.9
        # From: https://core.tcl.tk/tk/info/509cafafae
        #
        # Returns the style map for 'option' with any styles starting with
        # ('!disabled', '!selected', ...) filtered out.

        # style.map() returns an empty list for missing options, so this
        # should be future-safe.
        return [elm for elm in self.style.map('Treeview', query_opt=option)
                if elm[:2] != ('!disabled', '!selected')]
