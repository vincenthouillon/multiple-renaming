#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""Called from multiple_renaming.py"""

import sys
from tkinter import PhotoImage, Tk

from utils.constants import (ALERT_CHAR, ARGUMENTS_DICT, OPTIONS_DICT,
                             WINDOWS_PROHIBITED_CHAR)
from utils.utils import date_formatting
from utils.versions import __version__

from views.menubar import MenuBar
from views.parameters import Parameters
from views.statusbar import StatusBar
from views.treeview import Treeview

if sys.platform == "win32":
    from winsound import PlaySound, SND_ASYNC


class View(Tk):
    """Class main view.

    Args:
        Tk (object): Instance Tkinter.
    """

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.menubar = MenuBar(self, self.controller)
        self.treeview = Treeview(self)
        self.params = Parameters(self)
        self.statusbar = StatusBar(self)

        self._set_window_ui()
        self._populate_options()
        self._signals()

        self.arguments_dict = ARGUMENTS_DICT

    def _set_window_ui(self):
        """Global configuration of the main window."""
        self.title(f"Multiple Renaming - {__version__}")
        self.minsize(700, 540)
        self.geometry("700x540")

        if sys.platform == "win32":
            self.iconbitmap(r"./assets/icon.ico")
        else:
            self.iconphoto(True, PhotoImage(file=r"./assets/icon.png"))

    def _signals(self):
        self.treeview.tree.bind(
            "<Double-Button-1>",
            lambda event: self.controller.open_filenames())

        self.params.arguments_cbox.bind(
            "<<ComboboxSelected>>", self.arguments_callback)

        self.params.start_sbox.bind(
            "<ButtonRelease>",
            lambda event: self.params.filename_entry.focus())
        self.params.step_sbox.bind(
            "<ButtonRelease>",
            lambda event: self.params.filename_entry.focus())
        self.params.digits_sbox.bind(
            "<ButtonRelease>",
            lambda event: self.params.filename_entry.focus())

        self.params.date_cbox.bind(
            "<<ComboboxSelected>>",
            lambda event: self.params.filename_entry.focus())

        self.params.find_entry.bind(
            "<KeyRelease>", self.controller.search_and_replace)
        self.params.find_entry.bind(
            "<FocusIn>", self.controller.search_and_replace)

        self.params.replace_entry.bind(
            "<KeyRelease>", self.controller.search_and_replace)
        self.params.replace_entry.bind(
            "<KeyRelease BackSpace>", self.controller.search_and_replace)
        self.params.replace_entry.bind(
            "<FocusIn>", self.controller.search_and_replace)

        self.params.date_entry.bind(
            "<KeyRelease>", lambda event: self.controller.input_filename(
                self.params.filename_entry.get()))

        self.params.find_entry.bind(
            "<FocusIn>", self.params.clear_find_placeholder)
        self.params.find_entry.bind(
            "<FocusOut>", self.params.add_find_placeholder)
        self.params.replace_entry.bind(
            "<FocusIn>", self.params.clear_replace_placeholder)
        self.params.replace_entry.bind(
            "<FocusOut>", self.params.add_replace_placeholder)

        self.valid_filename = self.params.frame.register(
            self.controller.input_filename)
        self.params.filename_entry.config(
            validate="all", validatecommand=(self.valid_filename, "%P"))

        self.params.rename_btn.config(command=self.controller.rename)

    def activate_button(self, state="normal"):
        """Set state button rename.

        Keyword Arguments:
            state {str} -- "normal" or False (default: {"normal"})
        """
        if state == "normal":
            self.params.rename_btn.config(state="normal")
        else:
            self.params.rename_btn.config(state="disabled")

    def check_valid_characters_filename(self, name_modified):
        """Checks that the file name does not contain characters
        prohibited by Microsoft Windows.

        Arguments:
            name_modified {str} -- Filename
        """

        for char in WINDOWS_PROHIBITED_CHAR:
            if char in name_modified:
                self.statusbar.var_alert.set(
                    ALERT_CHAR)
                PlaySound("SystemAsterisk", SND_ASYNC)
                self.activate_button(False)
                break
            else:
                self.statusbar.var_alert.set("")
                self.activate_button()

    def display_treeview(self, data):
        """Populate treeview.

        Args:
            data (dict): Dict of data.
            tag (str, optional): If duplate files. Defaults to None.
        """
        self.treeview.tree.delete(*self.treeview.tree.get_children())

        _list = [d["new_name"] for d in data]

        if not _list:
            self.activate_button(False)

        _duplicates = set([fnane for fnane in _list if _list.count(fnane) > 1])

        for columns in data:
            if columns["new_name"] in _duplicates:
                self.treeview.tree.insert(
                    "", "end", values=list(columns.values()),
                    tag="ERR"
                )
                self.activate_button(False)
            else:
                self.treeview.tree.insert(
                    "", "end", values=list(columns.values())
                )

    def arguments_callback(self, event):
        """Application of argument functions.

        Arguments:
            event {dict} -- Bind event
        """
        for key, value in self.arguments_dict.items():
            if self.params.arguments_cbox.get() in value:
              self.controller.parse_filenames(argument=key)

    def _populate_options(self):
        """Filled the options menu."""
        entry = self.params.filename_entry
        for key, value in OPTIONS_DICT.items():
            self.params.menu_btn.menu.add_command(
                label=value,
                command=lambda k=key: entry.insert(entry.index("insert"), k)
            )

    def get_format_date(self):
        """Get date from widgets and formating this.

        Returns:
            tuple: Date formated.
        """
        date_format = date_formatting(
            self.params.date_cbox.get(),
            self.params.date_entry.get())
        return (date_format[0], date_format[1])

    def main(self):
        """Launch main interface."""
        self.mainloop()
