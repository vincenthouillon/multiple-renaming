#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from tkinter import *
from tkinter import ttk

from treeview import Treeview
from notebook import Notebook


class MultipleRenaming:
    def __init__(self, master):
        self.master = master
        self.configure()
        self.create_widgets()

    def configure(self):
        self.master.title("Renommage Multiple")
        self.master.minsize(600, 400)

        menu = Menu(self.master)
        self.master.config(menu=menu)

        fileMenu = Menu(menu, tearoff=False)
        fileMenu.add_command(label="Ouvrir")
        fileMenu.add_command(label="Quitter", command=self._exit)
        menu.add_cascade(label="Fichier", menu=fileMenu)

        editMenu = Menu(menu, tearoff=False)
        editMenu.add_command(label="Afficher la licence")
        editMenu.add_command(label="A propos")
        menu.add_cascade(label="Aide", menu=editMenu)

    def create_widgets(self):
        """ Add widgets. """
        Treeview(self.master)
        Notebook(self.master)

    def _exit(self):
        exit()


if __name__ == "__main__":
    root = Tk()
    app = MultipleRenaming(root)
    root.mainloop()
