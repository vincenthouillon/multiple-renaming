#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
from tkinter import *
from tkinter.filedialog import askopenfilenames

from widgets.notebook import Notebook
from widgets.statusbar import StatusBar
from widgets.treeview import Treeview


class MultipleRenaming:
    def __init__(self, master):
        self.master = master
        self.configure()
        self.create_widgets()

    def configure(self):
        self.master.title("Renommage Multiple")
        self.master.minsize(700, 540)

        menu = Menu(self.master)
        self.master.config(menu=menu)

        file_menu = Menu(menu, tearoff=False)
        file_menu.add_command(label="Ouvrir", command=self.get_filenames)
        file_menu.add_command(label="Quitter", command=_exit)
        menu.add_cascade(label="Fichier", menu=file_menu)

        edit_menu = Menu(menu, tearoff=False)
        edit_menu.add_command(label="Afficher la licence")
        edit_menu.add_command(label="A propos")
        menu.add_cascade(label="Aide", menu=edit_menu)

    def create_widgets(self):
        """ Add widgets. """
        Treeview(self.master)
        Notebook(self.master)
        StatusBar(self.master)

    def get_filenames(self):
        filenames = askopenfilenames()
        for f in filenames:
            statinfo = os.stat(f)
            print(f"{f} - {statinfo.st_size/1024 :0.3} Mo")


def _exit():
    exit()


if __name__ == "__main__":
    root = Tk()
    app = MultipleRenaming(root)
    root.mainloop()
