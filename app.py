#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import platform
from datetime import datetime
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

        if platform == "Darwin":
            file_menu.add_command(
                label="Ouvrir", accelerator="Command-O",
                underline=0, command=self.get_filenames)
            self.master.bind("<Command-o>", self.get_filenames)

            file_menu.add_command(
                label="Quitter", accelerator="Command-W", command=quit)
        else:
            file_menu.add_command(
                label="Ouvrir", accelerator="Ctrl-O",
                underline=0, command=self.get_filenames)
            self.master.bind("<Control-o>", self.get_filenames)

            file_menu.add_command(
                label="Quitter", accelerator="Alt-F4", command=quit)

        menu.add_cascade(label="Fichier", menu=file_menu)

        edit_menu = Menu(menu, tearoff=False)
        edit_menu.add_command(label="Afficher la licence")
        edit_menu.add_command(label="A propos")
        menu.add_cascade(label="Aide", menu=edit_menu)

    def start_count(self, event):
        print("Start updated:", self.notebook.sbox_start.get())
        self.notebook.entry_filename.focus()

    def step_count(self, event):
        print("Step updated:", self.notebook.sbox_step.get())
        self.notebook.entry_filename.focus()

    def lenght_count(self, event):
        print("Lenght updated:", self.notebook.sbox_len.get())
        self.notebook.entry_filename.focus()

    def formatted_date(self, event):
        self.notebook.entry_filename.focus()

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
        self.notebook.cbox_date.bind(
            "<<ComboboxSelected>>", self.formatted_date)

        # NOTE In progress
        self.valid = self.notebook.frame.register(self.is_valid)
        self.notebook.entry_filename.config(
            validate="all", validatecommand=(self.valid, "%d", "%i", "%P"))
        self.statusbar = StatusBar(self.master)

    def is_valid(self, d, i, P):
        # print(d, i, P)

        date_format = self.date_formatting()

        temp_filename = list()
        for fn in self.initial_filenames:
            temp_filename.append(os.path.splitext(os.path.basename(fn))[0])

        if "[n]" in P:
            for index, filename in enumerate(temp_filename):
                self.changed_filenames[index] = P.replace("[n]", filename)
            self.display_treeview()
        else:
            for index, dirname in enumerate(self.initial_filenames):
                filename, ext = os.path.splitext(os.path.basename(dirname))
                self.changed_filenames[index] = P
            self.display_treeview()

        if "[c]" in P:
            counter = int(self.notebook.sbox_start.get())
            for index, filename in enumerate(self.changed_filenames):
                formated_counter = f"{counter:0{self.notebook.sbox_len.get()}}"
                self.changed_filenames[index] = filename.replace(
                    "[c]", formated_counter)
                counter += int(self.notebook.sbox_step.get())
            self.display_treeview()

        if "[d]" in P:
            for index, filename in enumerate(self.changed_filenames):
                self.changed_filenames[index] = filename.replace(
                    "[d]", date_format)
            self.display_treeview()

        return True

    def date_formatting(self):
        # TODO Gestion des erreurs et limite des caractères
        now = datetime.now()
        date_gabarit = self.notebook.cbox_date.get()
        if "yyyy" in date_gabarit:
            date_gabarit = date_gabarit.replace("yyyy", now.strftime("%Y"))
        elif "yy" in date_gabarit:
            date_gabarit = date_gabarit.replace("yy", now.strftime("%y"))
        if "mm" in date_gabarit:
            date_gabarit = date_gabarit.replace("mm", now.strftime("%m"))
        if "dd" in date_gabarit:
            date_gabarit = date_gabarit.replace("dd", now.strftime("%d"))
        if "hh" in date_gabarit:
            date_gabarit = date_gabarit.replace("hh", now.strftime("%H"))
        if "nn" in date_gabarit:
            date_gabarit = date_gabarit.replace("nn", now.strftime("%M"))
        if "ss" in date_gabarit:
            date_gabarit = date_gabarit.replace("ss", now.strftime("%S"))
        return date_gabarit

    def get_filenames(self, *args):
        self.initial_filenames = askopenfilenames()

        self.changed_filenames = [
            os.path.splitext(os.path.basename(fn))[0]
            for fn in self.initial_filenames]

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
            extension = os.path.splitext(old_name)[1]
            name_modified = new_name + extension

            name_modified = self.arguments_parsing(argument, new_name, extension)

            # Treeview output
            size = f"{os.path.getsize(initial)/1024:.2f} Mo"

            self.treeview.tree.insert(
                "", "end", text=old_name, values=(name_modified, size))

    def arguments_parsing(self, arg, nn, ext):
        parser = {
            1: nn.lower() + ext,
            2: nn.upper() + ext,
            3: nn + ext.lower(),
            4: nn + ext.upper(),
            5: nn.lower() + ext.lower(),
            6: nn.upper() + ext.upper(),
            7: nn.title() + ext,
            8: nn.capitalize() + ext
        }

        for key, value in parser.items():
            if arg == key:
                return value

        return nn + ext

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
