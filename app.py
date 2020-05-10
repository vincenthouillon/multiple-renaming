#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
Copyright 2020 Vincent Houillon

GitHub: https://github.com/vincenthouillon/multiple_renaming
"""

import os
import platform
from datetime import datetime
from tkinter import *
from tkinter.filedialog import askopenfilenames
from tkinter.messagebox import showerror

from common.constants import ARGUMENTS_DICT, OPTIONS_DICT
from common.modules import Modules
from widgets.parameters import Parameters
from widgets.statusbar import StatusBar
from widgets.treeview import Treeview


class MultipleRenaming:

    def __init__(self, master):
        self.master = master
        self.configure()
        self.load_widgets()
        self.module = Modules()

        self.initial_filenames = list()
        self.changed_filenames = list()
        self.changed_filenames_copy = list()

        self.prohibited_characters = [
            "<", ">", "\\", "/", ":", "*", "?", "|", "\""]

    def configure(self):
        self.master.title("Renommage Multiple")
        self.master.minsize(700, 540)
        self.master.geometry("700x540")

        img = Image("photo", file=os.path.join("icons", "rename.png"))
        self.master.tk.call("wm", "iconphoto", self.master._w, img)

        menu = Menu(self.master)
        self.master.config(menu=menu)

        file_menu = Menu(menu, tearoff=False)

        if platform.system() == "Darwin":
            file_menu.add_command(
                label="Ouvrir", accelerator="Command-O",
                underline=0, command=self.open_filenames)
            self.master.bind("<Command-o>", self.open_filenames)

            file_menu.add_command(
                label="Quitter", accelerator="Command-W", command=quit)
        else:
            file_menu.add_command(
                label="Ouvrir", accelerator="Ctrl-O",
                underline=0, command=self.open_filenames)
            self.master.bind("<Control-o>", self.open_filenames)

            file_menu.add_command(
                label="Quitter", accelerator="Alt-F4", command=quit)

        menu.add_cascade(label="Fichier", menu=file_menu)

        edit_menu = Menu(menu, tearoff=False)
        edit_menu.add_command(label="Afficher la licence")
        edit_menu.add_command(label="A propos")
        menu.add_cascade(label="Aide", menu=edit_menu)

    def load_widgets(self):
        """ Load widgets and bindings event. """
        self.treeview = Treeview(self.master)
        self.params = Parameters(self.master)
        self.populate_options()
        # Binding
        self.params.cbox_arguments.bind(
            "<<ComboboxSelected>>", self.arguments_callback)
        self.params.sbox_start.bind(
            "<ButtonRelease>", lambda event: self.params.entry_filename.focus())
        self.params.sbox_step.bind(
            "<ButtonRelease>", lambda event: self.params.entry_filename.focus())
        self.params.sbox_len.bind(
            "<ButtonRelease>", lambda event: self.params.entry_filename.focus())
        self.params.cbox_date.bind(
            "<<ComboboxSelected>>", lambda event: self.params.entry_filename.focus())

        self.params.entry_search.bind(
            "<KeyRelease>", self.search_and_replace)

        self.params.entry_replace.bind(
            "<KeyRelease>", self.search_and_replace)
        self.params.entry_replace.bind(
            "<KeyRelease BackSpace>", self.search_and_replace)

        self.valid = self.params.frame.register(self.input_filename)
        self.params.entry_filename.config(
            validate="all", validatecommand=(self.valid, "%P"))
        self.statusbar = StatusBar(self.master)
        self.params.btn_rename.config(command=self.rename)

    def open_filenames(self):
        self.initial_filepath = askopenfilenames()
        self.initial_filenames = list()

        for basename in self.initial_filepath:
            self.initial_filenames.append(os.path.basename(basename))

        self.changed_filenames = self.initial_filenames[:]

        self.statusbar.lbl_count_files.config(
            text=f"{len(self.initial_filenames)} fichier(s)")
        self.display_treeview()

    def input_filename(self, P):
        """Check the content of the input widget to verify that it is valid
        with the rules of the application.

        Arguments:
            P {str} -- Value of the entry if the edit is allowed

        Returns:
            str -- Output text processed by application rules
        """

        user_input = P

        date_format = self.module.date_formatting(self.params.cbox_date.get())
        counter = int(self.params.sbox_start.get())

        for index, (initial, changed) in enumerate(
                zip(self.initial_filenames, self.changed_filenames)):
            filename, ext = os.path.splitext(initial)

            if "[n]" in user_input:
                temp_input = user_input.replace("[n]", filename)
                self.changed_filenames[index] = temp_input + ext
            else:
                temp_input = user_input
                self.changed_filenames[index] = user_input + ext

            if "[d]" in user_input:
                filename, ext = os.path.splitext(initial)
                temp_input = temp_input.replace("[d]", date_format)
                self.changed_filenames[index] = temp_input + ext

            if "[c]" in user_input:
                formated_counter = f"{counter:0{self.params.sbox_len.get()}}"
                temp_input = temp_input.replace("[c]", formated_counter)
                self.changed_filenames[index] = temp_input + ext
                counter += int(self.params.sbox_step.get())

            # Name from first character
            if re.findall(r"\[n\d+\]", user_input):
                re_findall = re.findall(r"\[n\d+\]", user_input)
                position = re_findall[0][2:len(re_findall)-2]

                temp_input = temp_input.replace(
                    re_findall[0], filename[0:int(position)]
                )
                self.changed_filenames[index] = temp_input + ext

            # Name from last character
            if re.findall(r"\[n-\d+\]", user_input):
                re_findall = re.findall(r"\[n-\d+\]", user_input)
                position = re_findall[0][3:len(re_findall)-2]

                nchar = len(filename)-int(position)
                # result = [condition is false, condition is true][condition]
                nchar = [0, nchar][nchar > 0]

                temp_input = temp_input.replace(
                    re_findall[0], filename[nchar:])
                self.changed_filenames[index] = temp_input + ext

            # Name from n character
            if re.findall(r"\[n,\d+\]", user_input):
                re_findall = re.findall(r"\[n,\d+\]", user_input)
                position = re_findall[0][3:len(re_findall)-2]

                temp_input = temp_input.replace(
                    re_findall[0], filename[int(position)-1:len(filename)])
                self.changed_filenames[index] = temp_input + ext

        self.display_treeview()
        return True

    def search_and_replace(self, event):
        search_expr = self.params.entry_search.get()
        replace_expr = self.params.entry_replace.get()

        if len(search_expr) > 0:
            self.changed_filenames = self.initial_filenames[:]
            for index, word in enumerate(self.initial_filenames):
                if search_expr in word:
                    self.changed_filenames[index] = word.replace(
                        search_expr, replace_expr)
        else:
            self.changed_filenames = self.initial_filenames[:]
        self.display_treeview()

    def rename(self):
        """Renaming files."""
        for index, (initial, modified) in enumerate(zip(self.initial_filenames,
                                                        self.changed_filenames)):
            dirname_initial = os.path.dirname(initial)
            basename_initial = os.path.basename(initial)
            extension_initial = os.path.splitext(basename_initial)[1]

            # Get the key from the arguments list
            for key, value in ARGUMENTS_DICT.items():
                if self.params.cbox_arguments.get() in value:
                    arg_key = key

            # Apply argument options
            modified = self.arguments_parsing(
                arg_key, modified, extension_initial)

            new_filename = os.path.join(dirname_initial, modified)

            try:
                os.rename(initial, new_filename)
            except OSError:
                showerror(
                    "Erreur", "La syntaxe du nom de fichier est incorrecte")
                break

            # Convert tuple to list.
            self.initial_filenames = list(self.initial_filenames)

            # Update renamed file
            self.initial_filenames[index] = new_filename
            self.changed_filenames_copy = self.changed_filenames[:]

        self.display_treeview()
        self.params.entry_filename.focus()

        if self.params.check_var.get():
            quit()

    def display_treeview(self, argument=None):
        """Management of the display of the treeview.

        Keyword Arguments:
            argument {int} -- Key to the arguments, to transform text into
            capital letters for example. (default: {None})
        """
        # Delete treeview
        self.treeview.tree.delete(*self.treeview.tree.get_children())

        for initial, changed in zip(
                self.initial_filepath, self.changed_filenames):

            old_name = os.path.basename(initial)
            new_name = os.path.basename(changed)

            if platform.system() == "Windows":
                self.module.check_valid_characters_filename(new_name)

            date_creation = datetime.fromtimestamp(os.path.getmtime(initial))
            date_creation_formated = datetime.strftime(
                date_creation, "%Y/%m/%d %H:%M:%S")

            date_modified = datetime.fromtimestamp(os.path.getctime(initial))
            date_modified_formated = datetime.strftime(
                date_modified, "%Y/%m/%d %H:%M:%S")

            location = os.path.abspath(initial)

            size = self.module.get_human_readable_size(
                os.path.getsize(initial))

            # Find duplicate files
            duplicate_files = set(
                [x for x in self.changed_filenames
                 if self.changed_filenames.count(x) > 1])

            if os.path.splitext(new_name)[0] in [x for x in duplicate_files]:
                self.treeview.tree.insert(
                    "", "end",
                    text=old_name,
                    values=(new_name, size, date_creation_formated,
                            date_modified_formated, location), tag="ERR")
                self.activate_button("disabled")
                continue
            else:
                self.treeview.tree.insert(
                    "", "end",
                    text=old_name,
                    values=(new_name, size, date_creation_formated,
                            date_modified_formated, location))
                self.activate_button("normal")

    # BUG Not used at the moment, to be implemented
    def activate_button(self, state="normal"):
        """Set state button rename.

        Keyword Arguments:
            state {str} -- "normal" or "disabled" (default: {"normal"})
        """
        if state == "normal":
            self.params.btn_rename.config(state="normal")
        else:
            self.params.btn_rename.config(state="disabled")

    def arguments_callback(self, event):
        for key, value in ARGUMENTS_DICT.items():
            if self.params.cbox_arguments.get() in value:
                self.display_treeview(key)

    def populate_options(self):
        entry = self.params.entry_filename
        for key, value in OPTIONS_DICT.items():
            self.params.mb.menu.add_command(
                label=value,
                command=lambda k=key: entry.insert(entry.index(INSERT), k)
            )
        entry.insert(0, "[n]")


if __name__ == "__main__":
    root = Tk()
    app = MultipleRenaming(root)
    root.mainloop()
