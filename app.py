#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from tkinter import *

from widgets.treeview import Treeview
from widgets.notebook import Notebook
from widgets.statusbar import StatusBar


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
        file_menu.add_command(label="Ouvrir")
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


def _exit():
    exit()


if __name__ == "__main__":
    root = Tk()
    app = MultipleRenaming(root)
    root.mainloop()
