#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
Copyright 2020 Vincent Houillon
This file is written by Vincent Houillon.
Redistribution or reuse is not permitted without express written consent.

GitHub: https://github.com/vincenthouillon/multiple_renaming
"""

import os
import platform
from datetime import datetime
from tkinter import *
from tkinter.filedialog import askopenfilenames
from tkinter.messagebox import showerror

from widgets.constants import ARGUMENTS_DICT, OPTIONS_DICT
from widgets.parameters import Parameters
from widgets.statusbar import StatusBar
from widgets.treeview import Treeview


class MultipleRenaming:

    def __init__(self, master):
        self.master = master
        self.configure()
        self.load_widgets()

        self.initial_filenames = list()
        self.changed_filenames = list()

        self.prohibited_characters = [
            "<", ">", "\\", "/", ":", "*", "?", "|", "\""]
        self.prohibited_filename = ["CON", "PRN", "AUX", "NUL", "COM1", "COM2",
                                    "COM3", "COM4", "COM5", "COM6", "COM7", "COM8",
                                    "COM9", "LPT1", "LPT2", "LPT3", "LPT4", "LPT5",
                                    "LPT6", "LPT7", "LPT8", "LPT9"]

    def configure(self):
        self.master.title("Renommage Multiple")
        self.master.minsize(700, 540)
        self.master.geometry("700x540")

        img = Image("photo", file="icons/rename.png")
        self.master.tk.call("wm", "iconphoto", self.master._w, img)

        menu = Menu(self.master)
        self.master.config(menu=menu)

        file_menu = Menu(menu, tearoff=False)

        if platform.system() == "Darwin":
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

    def load_widgets(self):
        """ Add widgets. """
        self.treeview = Treeview(self.master)
        self.parameters = Parameters(self.master)
        self.populate_options()
        # Binding
        self.parameters.cbox_arguments.bind(
            "<<ComboboxSelected>>", self.arguments_callback)
        self.parameters.sbox_start.bind(
            "<ButtonRelease>", lambda event: self.parameters.entry_filename.focus())
        self.parameters.sbox_step.bind(
            "<ButtonRelease>", lambda event: self.parameters.entry_filename.focus())
        self.parameters.sbox_len.bind(
            "<ButtonRelease>", lambda event: self.parameters.entry_filename.focus())
        self.parameters.cbox_date.bind(
            "<<ComboboxSelected>>", lambda event: self.parameters.entry_filename.focus())
        self.parameters.entry_replace.bind(
            "<KeyRelease>", self.search_and_replace)

        # NOTE In progress
        self.valid = self.parameters.frame.register(self.is_valid)
        self.parameters.entry_filename.config(
            validate="all", validatecommand=(self.valid, "%d", "%i", "%P"))
        self.statusbar = StatusBar(self.master)
        self.parameters.btn_rename.config(command=self.rename)

    # -------------------------------------------------------------------------
    # BUG Créer une fonction pour la recherche pour mettre à jour l'affichage
    # quand il n'y a rien dans le champ de saisie.

    def search_and_replace(self, event):
        search_expr = self.parameters.entry_search.get()
        replace_expr = self.parameters.entry_replace.get()
        self.parameters.entry_replace.focus()

        if len(search_expr) > 0 and len(replace_expr) > 0:
            for index, word in enumerate(self.changed_filenames_copy):
                if search_expr in word:
                    self.changed_filenames[index] = word.replace(
                        search_expr, replace_expr)
            self.display_treeview()
        else:
            self.changed_filenames = self.changed_filenames_copy[:]
            self.display_treeview()
    # -------------------------------------------------------------------------

    def rename(self):
        """Renaming files."""
        for index, (initial, modified) in enumerate(zip(self.initial_filenames,
                                                        self.changed_filenames)):
            dirname_initial = os.path.dirname(initial)
            basename_initial = os.path.basename(initial)
            filename_initial, extension_initial = os.path.splitext(
                basename_initial)

            # Get the key from the arguments list
            for key, value in ARGUMENTS_DICT.items():
                if self.parameters.cbox_arguments.get() in value:
                    arg_key = key

            # Apply argument options
            modified = self.arguments_parsing(
                arg_key, modified, extension_initial)

            new_filename = os.path.join(dirname_initial, modified)

            try:
                os.rename(initial, new_filename)
            except OSError:
                print("[-] La syntaxe du nom de fichier est incorrecte")
                showerror(
                    "Erreur", "La syntaxe du nom de fichier est incorrecte")
                break

            # Convert tuple to list.
            self.initial_filenames = list(self.initial_filenames)

            # Update renamed file
            self.initial_filenames[index] = new_filename

        try:
            self.display_treeview()
            self.parameters.entry_filename.focus()
        except FileNotFoundError:
            print("[-] Error: File Not Found!")

        if self.parameters.check_var.get():
            quit()

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

        # Option [nx]
        if re.findall(r"\[n\d+\]", P):
            re_findall = re.findall(r"\[n\d+\]", P)
            nx = re_findall[0][2:len(re_findall)-2]
            for index, filename in enumerate(temp_filename):
                self.changed_filenames[index] = P.replace(
                    re_findall[0], filename[0:int(nx)])
            self.display_treeview()

        # Option [n-x]
        if re.findall(r"\[n-\d+\]", P):
            re_findall = re.findall(r"\[n-\d+\]", P)
            nx = re_findall[0][3:len(re_findall)-2]
            for index, filename in enumerate(temp_filename):
                if len(filename) >= int(nx):
                    self.changed_filenames[index] = P.replace(
                        re_findall[0], filename[len(filename)-int(nx):])
                else:
                    self.changed_filenames[index] = filename
            self.display_treeview()

        # Option [n,x]
        if re.findall(r"\[n,\d+\]", P):
            re_findall = re.findall(r"\[n,\d+\]", P)
            nx = re_findall[0][3:len(re_findall)-2]
            for index, filename in enumerate(temp_filename):
                if len(filename) >= int(nx):
                    self.changed_filenames[index] = P.replace(
                        re_findall[0], filename[int(nx)-1:len(filename)])
                else:
                    self.changed_filenames[index] = filename
            self.display_treeview()

        if "[c]" in P:
            counter = int(self.parameters.sbox_start.get())
            for index, filename in enumerate(self.changed_filenames):
                formated_counter = f"{counter:0{self.parameters.sbox_len.get()}}"
                self.changed_filenames[index] = filename.replace(
                    "[c]", formated_counter)
                counter += int(self.parameters.sbox_step.get())
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
        date_format = self.parameters.cbox_date.get()
        if "yyyy" in date_format:
            date_format = date_format.replace("yyyy", now.strftime("%Y"))
        elif "yy" in date_format:
            date_format = date_format.replace("yy", now.strftime("%y"))
        if "mm" in date_format:
            date_format = date_format.replace("mm", now.strftime("%m"))
        if "dd" in date_format:
            date_format = date_format.replace("dd", now.strftime("%d"))
        if "hh" in date_format:
            date_format = date_format.replace("hh", now.strftime("%H"))
        if "nn" in date_format:
            date_format = date_format.replace("nn", now.strftime("%M"))
        if "ss" in date_format:
            date_format = date_format.replace("ss", now.strftime("%S"))
        return date_format

    def get_filenames(self, *args):
        self.initial_filenames = askopenfilenames()

        self.changed_filenames = [
            os.path.splitext(os.path.basename(fn))[0]
            for fn in self.initial_filenames]

        self.changed_filenames_copy = self.changed_filenames[:]

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

            name_modified = self.arguments_parsing(
                argument, new_name, extension)

            if platform.system() == "Windows":
                self.check_valid_characters_filename(name_modified)

            date_creation = datetime.fromtimestamp(os.path.getmtime(initial))
            date_creation_formated = datetime.strftime(
                date_creation, "%Y/%m/%d %H:%M:%S")

            date_modified = datetime.fromtimestamp(os.path.getctime(initial))
            date_modified_formated = datetime.strftime(
                date_modified, "%Y/%m/%d %H:%M:%S")

            location = os.path.abspath(initial)

            size = self.get_human_readable_size(os.path.getsize(initial))

            self.treeview.tree.insert(
                "", "end", text=old_name, values=(name_modified, size, date_creation_formated, date_modified_formated, location))

    def get_human_readable_size(self, size, precision=2):
        """Convert n bytes into a human readable string based on format.

        Arguments:
            size {float} -- File size

        Keyword Arguments:
            precision {int} -- Number of digits after the decimal point. (default: {2})

        Returns:
            [type] -- [description]
        """
        suffixes = ['o', 'Ko', 'Mo', 'Go', 'To']
        suffix_index = 0
        while size > 1024 and suffix_index < 4:
            suffix_index += 1  # increment the index of the suffix
            size = size/1024.0  # apply the division
        return "%.*f %s" % (precision, size, suffixes[suffix_index])

    def check_valid_characters_filename(self, name_modified):
        for char in self.prohibited_characters:
            if char in name_modified:
                self.parameters.btn_rename.config(state="disabled")
                showerror(
                    "Erreur",
                    "Un nom de fichier ne peut pas contenir les caractères \
            suivants : \ / : * ? \" < > | ")
                break
            else:
                self.parameters.btn_rename.config(state="normal")

    def arguments_parsing(self, arg, new_name, ext):
        parser = {
            1: new_name.lower() + ext,
            2: new_name.upper() + ext,
            3: new_name + ext.lower(),
            4: new_name + ext.upper(),
            5: new_name.lower() + ext.lower(),
            6: new_name.upper() + ext.upper(),
            7: new_name.title() + ext,
            8: new_name.capitalize() + ext
        }

        for key, value in parser.items():
            if arg == key:
                return value
        else:
            return new_name + ext

    def arguments_callback(self, event):
        for key, value in ARGUMENTS_DICT.items():
            if self.parameters.cbox_arguments.get() in value:
                self.display_treeview(key)

    def populate_options(self):
        entry = self.parameters.entry_filename
        for key, value in OPTIONS_DICT.items():
            self.parameters.mb.menu.add_command(
                label=value,
                command=lambda k=key: entry.insert(entry.index(INSERT), k)
            )
        entry.insert(0, "[n]")


if __name__ == "__main__":
    root = Tk()
    app = MultipleRenaming(root)
    root.mainloop()
