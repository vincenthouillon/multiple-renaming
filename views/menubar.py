#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# pylint: disable=undefined-variable
# flake8: noqa: F821

"""Called from views.view"""

import sys
import webbrowser
from tkinter import Menu, PhotoImage

from utils import versions
from utils.utils import set_language
from views.about import About


class MenuBar:
    """Display menubar."""

    def __init__(self, parent, controller):
        """Setting bar menu."""
        self.parent = parent
        self.controller = controller

        self.about = About
        self.load_images()
        self.setui_menu()

    def load_images(self):
        """Load flags image."""
        self.img_fr = PhotoImage(file=r"./assets/fr.png")
        self.img_en = PhotoImage(file=r"./assets/en.png")

    def setui_menu(self):
        """Make widget menu."""
        menu = Menu(self.parent)
        self.parent.config(menu=menu)

        file_menu = Menu(menu, tearoff=False)

        if sys.platform == "darwin":
            file_menu.add_command(
                label=_("Open"), accelerator="Command-O",
                underline=0, command=self.controller.open_filenames)
            self.parent.bind("<Command-o>",
                             lambda event: self.controller.open_filenames())

            file_menu.add_command(
                label=_("Exit"), accelerator="Command-W",
                command=self.parent.destroy)
        else:
            file_menu.add_command(
                label=_("Open"), accelerator="Ctrl-O",
                underline=0, command=self.controller.open_filenames)
            self.parent.bind("<Control-o>",
                             lambda event: self.controller.open_filenames())

            file_menu.add_command(
                label=_("Exit"), accelerator="Alt-F4", command=sys.exit)

        menu.add_cascade(label=_("File"), menu=file_menu)

        lang_menu = Menu(menu, tearoff=False)
        lang_menu.add_command(
            label=_("French"),
            image=self.img_fr,
            compound="left",
            command=lambda: set_language("fr"))
        lang_menu.add_command(
            label=_("English"),
            image=self.img_en,
            compound="left",
            command=lambda: set_language("en"))
        menu.add_cascade(label="Language", menu=lang_menu)

        edit_menu = Menu(menu, tearoff=False)
        edit_menu.add_command(
            label=_("Website"),
            command=lambda: webbrowser.open(versions.__website__)
        )
        edit_menu.add_command(label=_("About"),
                              command=lambda: self.about(self.parent))
        menu.add_cascade(label=_("Help"), menu=edit_menu)
