#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# pylint: disable=undefined-variable
# pylint: disable=unused-argument
# flake8: noqa: F821

"""Called from views/view."""

from tkinter import IntVar, Menu, ttk

from _datetime import datetime
from utils.constants import ARGUMENTS_DICT, DATE_FORMAT


class Parameters:
    """Display parameters section."""

    def __init__(self, parent):
        self.parent = parent

        self.close_var = IntVar(value=0)

        self._set_global_ui()
        self._make_filename_widgets()
        self._make_find_replace_widgets()
        self._make_counter_widgets()
        self._make_timestamp_widgets()
        self._make_buttons_widgets()

    def _set_global_ui(self):
        """Set global widgets."""
        self.frame = ttk.Frame(self.parent, padding=(10, 10, 0, 5))
        self.frame.pack(fill="both")
        # LEFT PANEL
        self.left_panel = ttk.Frame(self.frame)
        self.left_panel.pack(side="left", fill="both", expand=True)
        # RIGHT PANEL
        self.right_panel = ttk.Frame(self.frame)
        self.right_panel.pack(fill="both", padx=10)

    def _make_filename_widgets(self):
        """Create and set 'method' and 'arguments' widgets."""
        method_lframe = ttk.LabelFrame(
            self.left_panel, text=_("Method"), padding=(5, 0, 5, 10))
        method_lframe.pack(fill="x", expand=True)

        filename_frm = ttk.Frame(method_lframe)
        filename_frm.pack(fill="x")
        filename_lbl = ttk.Label(
            filename_frm, text=_("Filename:"), foreground="grey")
        filename_lbl.pack(fill="x")
        self.filename_entry = ttk.Entry(filename_frm)
        self.filename_entry.insert(0, "[n]")
        self.filename_entry.pack(
            side="left", fill="x", expand=True)
        self.menu_btn = ttk.Menubutton(filename_frm, text="⚙️")
        self.menu_btn.pack(side="left")
        self.menu_btn.menu = Menu(self.menu_btn, tearoff=False)
        self.menu_btn["menu"] = self.menu_btn.menu

        arguments_frm = ttk.Frame(method_lframe)
        arguments_frm.pack(fill="x")
        arguments_lbl = ttk.Label(
            arguments_frm, text=_("Argument:"), foreground="grey")
        arguments_lbl.pack(fill="x")
        self.arguments_cbox = ttk.Combobox(
            arguments_frm,
            value=list(ARGUMENTS_DICT.values()),
            state='readonly')
        self.arguments_cbox.current(0)
        self.arguments_cbox.pack(fill="x")

    def _make_find_replace_widgets(self):
        """Create and set 'search & replace' widgets."""
        find_lframe = ttk.LabelFrame(
            self.left_panel, text=_("Find and replace"), padding=(5, 0, 5, 10))
        find_lframe.pack(fill="x", expand=True, pady=5)

        find_frm = ttk.Frame(find_lframe)
        find_frm.pack(fill="x")
        self.find_entry = ttk.Entry(find_frm, foreground="grey")
        self.find_entry.insert(0, _("Find..."))
        self.find_entry.pack(fill="x", pady=5)

        replace_frm = ttk.Frame(find_lframe)
        replace_frm.pack(fill="x")
        self.replace_entry = ttk.Entry(replace_frm, foreground="grey")
        self.replace_entry.insert(0, _("Replace..."))
        self.replace_entry.pack(fill="x")

    def _make_counter_widgets(self):
        """Create and set counter widgets."""
        counter_lframe = ttk.LabelFrame(
            self.right_panel, text=_("Counter"), padding=(5, 5, 5, 12))
        counter_lframe.pack(fill="x")

        start_frm = ttk.Frame(counter_lframe)
        start_frm.pack(fill="x")
        start_lbl = ttk.Label(start_frm, text=_("Start at:"))
        start_lbl.pack(anchor="w", side="left")
        self.start_sbox = ttk.Spinbox(start_frm, from_=0, to=1000, width=6)
        self.start_sbox.insert(0, 1)
        self.start_sbox.pack(side="right")

        step_frm = ttk.Frame(counter_lframe)
        step_frm.pack(fill="x", pady=2)
        step_lbl = ttk.Label(step_frm, text=_("Step by:"))
        step_lbl.pack(anchor="w", side="left")
        self.step_sbox = ttk.Spinbox(step_frm, from_=1, to=100, width=6)
        self.step_sbox.insert(0, 1)
        self.step_sbox.pack(side="right", pady=5)

        digits_frm = ttk.Frame(counter_lframe)
        digits_frm.pack(fill="x")
        digits_lbl = ttk.Label(digits_frm, text=_("Digits:"))
        digits_lbl.pack(side="left")
        self.digits_sbox = ttk.Spinbox(digits_frm, from_=0, to=5, width=6)
        self.digits_sbox.insert(0, 2)
        self.digits_sbox.pack(side="right")

    def _make_timestamp_widgets(self):
        """Create and set timestamp widgets."""
        date_lframe = ttk.LabelFrame(
            self.right_panel, text=_("Timestamp"), padding=(5, 0, 5, 10))
        date_lframe.pack(expand=True, fill="x", pady=5)

        self.date_entry = ttk.Entry(date_lframe)
        now = datetime.now()
        self.date_entry.insert(0, now.strftime("%d/%m/%Y"))
        self.date_entry.pack(fill="x", pady=5)

        self.date_cbox = ttk.Combobox(date_lframe, values=DATE_FORMAT)
        self.date_cbox.current(0)
        self.date_cbox.pack(anchor="w", fill="x")

    def _make_buttons_widgets(self):
        """Create and set buttons."""
        button_frm = ttk.Frame(self.parent, padding=(0, 0, 10, 10))
        button_frm.pack(fill="x")
        txt_btn = "✔️ " + _("Rename")
        self.rename_btn = ttk.Button(button_frm, text=txt_btn)
        self.rename_btn.pack(side="right")

        self.check_var = ttk.Checkbutton(
            button_frm, text=_("Close after rename"),
            variable=self.close_var, onvalue=1, offvalue=0)
        self.check_var.pack(side="right", padx=10)

    def clear_find_placeholder(self, event):
        """Remove placeholder from entry find.

        Args:
            event (dict): Event dict.
        """
        if self.find_entry.get() == _("Find..."):
            self.find_entry.delete(0, "end")
        self.find_entry.configure(foreground="black")

    def add_find_placeholder(self, event):
        """Add placeholder into entry find.

        Args:
            event (dict): Event dict.
        """
        if not self.find_entry.get():
            self.find_entry.configure(foreground="grey")
            self.find_entry.insert(0, _("Find..."))

    def clear_replace_placeholder(self, event):
        """"Remove placeholder from entry replace.

        Args:
            event (dict): Event dict.
        """
        if self.replace_entry.get() == _("Replace..."):
            self.replace_entry.delete(0, "end")
        self.replace_entry.configure(foreground="black")

    def add_replace_placeholder(self, event):
        """Add placeholder into entry replace.

        Args:
            event (dict): Event dict.
        """
        if not self.replace_entry.get():
            self.replace_entry.configure(foreground="grey")
            self.replace_entry.insert(0, _("Replace..."))
