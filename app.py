#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
from tkinter import *
from tkinter.filedialog import askopenfilenames

from widgets.constants import ARGUMENTS_DICT, OPTIONS_DICT
from widgets.notebook import Notebook
from widgets.statusbar import StatusBar
from widgets.treeview import Treeview


class MultipleRenaming:

    def __init__(self, master):
        self.master = master
        self.configure()
        self.load_widgets()

        self.initial_filenames = list()
        self.changed_filenames = list()

    def configure(self):
        self.master.title("Renommage Multiple")
        self.master.minsize(700, 540)

        menu = Menu(self.master)
        self.master.config(menu=menu)

        file_menu = Menu(menu, tearoff=False)
        file_menu.add_command(
            label="Ouvrir", accelerator="Command-O",
            underline=0, command=self.get_filenames)
        file_menu.add_command(
            label="Quitter", accelerator="Command-W", command=quit)
        menu.add_cascade(label="Fichier", menu=file_menu)

        edit_menu = Menu(menu, tearoff=False)
        edit_menu.add_command(label="Afficher la licence")
        edit_menu.add_command(label="A propos")
        menu.add_cascade(label="Aide", menu=edit_menu)

        # Binding
        self.master.bind("<Command-o>", self.get_filenames)

    def start_count(self, event):
        print("Start:", self.notebook.sbox_start.get())

    def step_count(self, event):
        print("Step:", self.notebook.sbox_step.get())

    def lenght_count(self, event):
        print("Lenght:", self.notebook.sbox_len.get())

    def load_widgets(self):
        """ Add widgets. """
        self.treeview = Treeview(self.master)
        self.notebook = Notebook(self.master)
        self.populate_options()
        # Binding
        self.notebook.cbox_arguments.bind(
            "<<ComboboxSelected>>", self.arguments_callback)
        self.notebook.sbox_start.bind("<ButtonRelease>", self.start_count)
        self.notebook.sbox_step.bind("<ButtonRelease>", self.step_count)
        self.notebook.sbox_len.bind("<ButtonRelease>", self.lenght_count)

        # NOTE In progress
        self.valid = self.notebook.frame.register(self.is_valid)
        self.notebook.entry_filename.config(
            validate="all", validatecommand=(self.valid, "%d", "%i", "%P"))
        self.statusbar = StatusBar(self.master)

    def is_valid(self, d, i, P):
        # print(d, i, P)
        # NOTE Testing
        if "[c]" in P:
            print(self.notebook.sbox_start.get())
        if "[n]" not in P:
            self.changed_filenames = [""] * len(self.initial_filenames)
            self.display_treeview()
        else:
            self.changed_filenames = self.initial_filenames[:]
            self.display_treeview(self.notebook.cbox_arguments.current())
        return True

    def get_filenames(self, *args):
        self.initial_filenames = askopenfilenames()

        self.changed_filenames = [os.path.basename(
            fn) for fn in self.initial_filenames]

        self.statusbar.lbl_count_files.config(
            text=f"{len(self.initial_filenames)} fichier(s)")
        self.display_treeview()

    def display_treeview(self, argument=None):
        # Delete treeview
        self.treeview.tree.delete(*self.treeview.tree.get_children())

        for initial, changed in zip(
                self.initial_filenames, self.changed_filenames):
            old_name = os.path.basename(initial)
            new_name = os.path.basename(changed)
            nn_filename = os.path.splitext(new_name)[0]
            nn_extension = os.path.splitext(old_name)[1]
            name_modified = nn_filename + nn_extension

            if argument == 1:
                name_modified = nn_filename.lower() + nn_extension
            elif argument == 2:
                name_modified = nn_filename.upper() + nn_extension
            elif argument == 3:
                name_modified = nn_filename + nn_extension.lower()
            elif argument == 4:
                name_modified = nn_filename + nn_extension.upper()
            elif argument == 5:
                name_modified = new_name.lower()
            elif argument == 6:
                name_modified = new_name.upper()
            elif argument == 7:
                name_modified = nn_filename.title() + nn_extension
            elif argument == 8:
                name_modified = nn_filename.capitalize() + nn_extension

            # Treeview output
            size = f"{os.path.getsize(initial)/1024:.2f} Mo"

            self.treeview.tree.insert(
                "", "end", text=old_name, values=(name_modified, size))

    def arguments_callback(self, event):
        for key, value in ARGUMENTS_DICT.items():
            if self.notebook.cbox_arguments.get() in value:
                self.display_treeview(key)

    def populate_options(self):
        entry = self.notebook.entry_filename
        for key, value in OPTIONS_DICT.items():
            self.notebook.mb.menu.add_command(
                label=value,
                command=lambda k=key: entry.insert(entry.index(INSERT), k)
            )
        entry.insert(0, "[n]")


if __name__ == "__main__":
    root = Tk()
    app = MultipleRenaming(root)
    root.mainloop()
