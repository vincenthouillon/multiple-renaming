#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# pylint: disable=undefined-variable

"""Called from viewq.view."""

import sys
import webbrowser
from tkinter import Frame, Label, PhotoImage, Toplevel, ttk

from utils import versions


class About:
    """Show about window."""

    def __init__(self, parent):
        self.parent = parent
        self._setup_ui()
        self._setup_widgets()

    def _setup_ui(self):
        """About window toplevel."""
        self.about = Toplevel()
        self.about.resizable(False, False)
        self.about.title(_("About"))
        self.about.transient(self.parent)

        # Set position TopLevel
        pos_x = self.parent.winfo_x()
        pos_y = self.parent.winfo_y()
        self.about.geometry("+%d+%d" % (pos_x + 200, pos_y + 200))

        if sys.platform == "win32":
            self.about.iconbitmap(r"./assets/icon.ico")
        else:
            self.about.iconphoto(True, PhotoImage(file=r"./assets/icon.png"))

    def _setup_widgets(self):
        frame = Frame(self.about)
        frame.pack(pady=20, padx=40)

        title = Label(frame, text="Multiple Renaming", font=("sans-serif", 16))
        title.pack()

        subtitle = Label(frame, text="File renaming utility.",
                         font=("sans-serif", 12))
        subtitle.pack()

        version_text = f"Version {versions.__version__}"
        version = Label(frame, text=version_text)
        version.pack()

        link_lbl = Label(
            frame, text="Website", fg="blue", cursor="hand2")
        link_lbl.pack()
        link_lbl.bind(
            "<Button-1>", lambda e: webbrowser.open_new(versions.__website__))

        ttk.Separator(frame, orient="horizontal").pack(fill="x", pady=10)

        _license = Label(frame, text="Copyright© 2020 - Vincent Houillon",
                         font=("sans-serif", 8))
        _license.pack()
