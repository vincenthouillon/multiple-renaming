#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""Multiple Renaming

File renaming application written in Python and using
only the standard library.

Program tested on Windows 10 and macOS Catalina with the
following Python versions:

- Python 3.7.4
- Python 3.8.2
"""

import configparser
import os
import platform
import re
import sys
import webbrowser
from datetime import datetime
from tkinter import INSERT, Image, Menu, Tk, PhotoImage
from tkinter.filedialog import askopenfilenames

from src.display import Display
from src.modules import Modules
from widgets.parameters import Parameters
from widgets.statusbar import StatusBar
from widgets.treeview import Treeview

__author__ = "Vincent Houillon"
__website__ = r"https://github.com/vincenthouillon/multiple_renaming"
__version__ = "0.8"


class MultipleRenaming:
    """Application to rename files."""
    # pylint: disable=too-many-instance-attributes

    def __init__(self, master):
        self.master = master
        self.configure()
        self.load_menu()
        self.load_widgets()
        self.modules = Modules()

        self.initial_filenames = list()
        self.changed_filenames = list()
        self.initial_filepath = list()
        self.replace_filename = list()

    def configure(self):
        """Definition of the title, size and icon of the application."""
        self.master.title("Multiple Renaming")
        self.master.minsize(700, 540)
        self.master.geometry("700x540")

        self.master.iconphoto(True, PhotoImage(file=r"icons/icon.png"))

        # Load and apply settings
        config = configparser.ConfigParser()
        config.read("config.ini")
        lng = config["language"]["language"]

        Display.set_language(lng)
        self.display = Display()

    def load_menu(self):
        """Setting toolbar."""
        menu = Menu(self.master)
        self.master.config(menu=menu)

        file_menu = Menu(menu, tearoff=False)

        toolbar = self.display.TOOLBAR

        if platform.system() == "Darwin":
            file_menu.add_command(
                label=toolbar["open"], accelerator="Command-O",
                underline=0, command=self.open_filenames)
            self.master.bind("<Command-o>", self.open_filenames)

            file_menu.add_command(
                label=toolbar["exit"], accelerator="Command-W", command=self.master.destroy)
        else:
            file_menu.add_command(
                label=toolbar["open"], accelerator="Ctrl-O",
                underline=0, command=self.open_filenames)
            self.master.bind("<Control-o>", self.open_filenames)

            file_menu.add_command(
                label=toolbar["exit"], accelerator="Alt-F4", command=sys.exit)

        menu.add_cascade(label=toolbar["file"], menu=file_menu)

        lang_menu = Menu(menu, tearoff=False)
        lang_menu.add_command(
            label=toolbar["french"],
            command=lambda: self.modules.set_language("fr"))
        lang_menu.add_command(
            label=toolbar["english"],
            command=lambda: self.modules.set_language("en"))
        menu.add_cascade(label="Language", menu=lang_menu)

        edit_menu = Menu(menu, tearoff=False)
        edit_menu.add_command(label=toolbar["website"],
                              command=lambda: webbrowser.open(__website__))
        edit_menu.add_command(label=toolbar["about"])
        menu.add_cascade(label=toolbar["help"], menu=edit_menu)

    def load_widgets(self):
        """Load widgets and bindings event."""
        self.treeview = Treeview(self.master)
        self.params = Parameters(self.master)
        self.populate_options()
        # Binding
        self.treeview.tree.bind(
            "<Double-Button-1>",
            lambda event: self.open_filenames())

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
        self.params.entry_search.bind(
            "<FocusIn>", self.search_and_replace)

        self.params.entry_replace.bind(
            "<KeyRelease>", self.search_and_replace)
        self.params.entry_replace.bind(
            "<KeyRelease BackSpace>", self.search_and_replace)
        self.params.entry_replace.bind(
            "<FocusIn>", self.search_and_replace)

        self.valid = self.params.frame.register(self.input_filename)
        self.params.entry_filename.config(
            validate="all", validatecommand=(self.valid, "%P"))
        self.statusbar = StatusBar(self.master)
        self.params.btn_rename.config(command=self.rename)

    def open_filenames(self):
        """Open files and display the number in the status bar."""
        self.initial_filepath = askopenfilenames()
        self.initial_filenames = list()

        for basename in self.initial_filepath:
            self.initial_filenames.append(basename)

        self.changed_filenames = self.initial_filenames[:]
        self.replace_filename = self.initial_filenames[:]

        txt = self.display.STATUSBAR["nb_files"]
        self.statusbar.lbl_count_files.config(
            text=f"{len(self.initial_filenames)} {txt} |")
        self.display_treeview()

    def input_filename(self, P):
        """Check the content of the input widget to verify that it is valid
        with the rules of the application.

        Arguments:
            P {str} -- Value of the entry if the edit is allowed

        Returns:
            str -- Output text processed by application rules
        """
        # pylint: disable=invalid-name, disable=too-many-locals
        # pylint: disable=too-many-statements

        user_input = P

        date_format = self.modules.date_formatting(self.params.cbox_date.get())
        counter = int(self.params.sbox_start.get())

        if platform.system() == "Windows":
            self.check_valid_characters_filename(user_input)

        for index, initial in enumerate(self.initial_filenames):
            dirname, filename = os.path.split(initial)
            filename, ext = os.path.splitext(filename)

            if "[n]" in user_input:
                temp_input = user_input.replace("[n]", filename)
                new_path = os.path.join(dirname, temp_input + ext)
                self.changed_filenames[index] = new_path
            else:
                temp_input = user_input
                new_path = os.path.join(dirname, temp_input + ext)
                self.changed_filenames[index] = new_path

            if "[d]" in user_input:
                temp_input = temp_input.replace("[d]", date_format)
                new_path = os.path.join(dirname, temp_input + ext)
                self.changed_filenames[index] = new_path

            if "[c]" in user_input:
                formated_counter = f"{counter:0{self.params.sbox_len.get()}}"
                temp_input = temp_input.replace("[c]", formated_counter)
                new_path = os.path.join(dirname, temp_input + ext)
                self.changed_filenames[index] = new_path
                counter += int(self.params.sbox_step.get())

            # Name from first character [nX]
            if re.findall(r"\[n\d+\]", user_input):
                re_findall = re.findall(r"\[n\d+\]", user_input)
                position = re_findall[0][2:len(re_findall)-2]

                len_dirname = len(os.path.dirname(filename))

                temp_input = temp_input.replace(
                    re_findall[0],
                    filename[len_dirname:len_dirname + int(position)])

                new_filename = os.path.join(
                    dirname + os.sep + temp_input + ext)

                self.changed_filenames[index] = new_filename

            # Name from last character [n-X]
            if re.findall(r"\[n-\d+\]", user_input):
                re_findall = re.findall(r"\[n-\d+\]", user_input)
                position = re_findall[0][3:len(re_findall)-2]

                nchar = len(filename)-int(position)
                # result = [condition is false, condition is true][condition]
                nchar = [0, nchar][nchar > 0]

                len_dirname = len(os.path.dirname(filename)) + 1

                temp_input = temp_input.replace(
                    re_findall[0], filename[nchar:])

                new_filename = os.path.join(
                    dirname + os.sep + temp_input + ext)

                self.changed_filenames[index] = new_filename

            # Name from n character [n,X]
            if re.findall(r"\[n,\d+\]", user_input):
                re_findall = re.findall(r"\[n,\d+\]", user_input)
                position = re_findall[0][3:len(re_findall)-2]

                len_dirname = len(os.path.dirname(filename))

                temp_input = temp_input.replace(
                    re_findall[0], filename[len_dirname + int(position):])

                new_filename = os.path.join(
                    dirname + os.sep + temp_input + ext)

                self.changed_filenames[index] = new_filename

        self.replace_filename = self.changed_filenames[:]

        self.display_treeview()
        return True

    def search_and_replace(self, event):
        """Search and replace function.

        Arguments:
            event {dict} -- Bind event.
        """
        # pylint: disable=unused-argument

        search_expr = self.params.entry_search.get()
        replace_expr = self.params.entry_replace.get()

        if platform.system() == "Windows":
            self.check_valid_characters_filename(replace_expr)

        if len(search_expr) > 0:
            self.changed_filenames = self.replace_filename[:]
            for index, word in enumerate(self.replace_filename):
                if search_expr in word:
                    self.changed_filenames[index] = word.replace(
                        search_expr, replace_expr)
        else:
            self.changed_filenames = self.replace_filename[:]
        self.display_treeview()

    def rename(self):
        """Execute file renaming."""
        for index, (initial, modified) in enumerate(zip(self.initial_filenames,
                                                        self.changed_filenames)):
            dirname = os.path.dirname(initial)
            basename_initial = os.path.basename(initial)
            extension_initial = os.path.splitext(basename_initial)[1]

            # Get the key from the arguments list
            for key, value in self.display.ARGUMENTS_DICT.items():
                if self.params.cbox_arguments.get() in value:
                    arg_key = key

            # Apply argument options
            modified = self.modules.arguments_parsing(
                arg_key,
                os.path.splitext(modified)[0],
                extension_initial)

            os.rename(initial, os.path.join(dirname, modified))

            # Convert tuple to list.
            self.initial_filenames = list(self.initial_filenames)

            # Update renamed file
            self.initial_filenames[index] = os.path.join(dirname, modified)

        self.display_treeview()
        self.params.entry_filename.focus()

        if self.params.check_var.get():
            sys.exit()

    def display_treeview(self, argument=None):
        """Management of the display of the treeview.

        Keyword Arguments:
            argument {int} -- Key to the arguments, to transform text into
            capital letters for example. (default: {None})
        """
        # pylint: disable=consider-using-set-comprehension, unnecessary-comprehension
        # pylint: disable=no-else-break, no-else-continue

        # Delete treeview content
        self.treeview.tree.delete(*self.treeview.tree.get_children())

        for initial, changed in zip(
                self.initial_filenames, self.changed_filenames):

            old_name = os.path.basename(initial)
            new_name, ext = os.path.splitext(os.path.basename(changed))

            name_modified = self.modules.arguments_parsing(
                argument, new_name, ext)

            date_creation = datetime.fromtimestamp(os.path.getmtime(initial))
            date_creation_formated = datetime.strftime(
                date_creation, "%Y/%m/%d %H:%M:%S")

            date_modified = datetime.fromtimestamp(os.path.getctime(initial))
            date_modified_formated = datetime.strftime(
                date_modified, "%Y/%m/%d %H:%M:%S")

            location = os.path.abspath(initial)

            size = self.modules.get_human_readable_size(
                os.path.getsize(initial))

            # Find an empty name and disable button "rename"
            if len(os.path.splitext(name_modified)[1]) <= 0:
                self.activate_button(False)

            # Find duplicate files
            duplicate_files = set(
                [x for x in self.changed_filenames
                 if self.changed_filenames.count(x) > 1])

            if changed in [x for x in duplicate_files]:
                self.treeview.tree.insert(
                    "", "end",
                    text=old_name,
                    values=(name_modified, size, date_creation_formated,
                            date_modified_formated, location), tag="ERR")
                self.activate_button(False)
                continue
            else:
                self.treeview.tree.insert(
                    "", "end",
                    text=old_name,
                    values=(name_modified, size, date_creation_formated,
                            date_modified_formated, location))
                if platform.system() == "Darwin":
                    self.activate_button()

    def activate_button(self, state="normal"):
        """Set state button rename.

        Keyword Arguments:
            state {str} -- "normal" or False (default: {"normal"})
        """
        if state == "normal":
            self.params.btn_rename.config(state="normal")
        else:
            self.params.btn_rename.config(state="disabled")

    def check_valid_characters_filename(self, name_modified):
        """Checks that the file name does not contain characters
        prohibited by Microsoft Windows.

        Arguments:
            name_modified {str} -- Filename
        """
        # pylint: disable=import-outside-toplevel, disable=import-error
        # pylint: disable=no-else-break

        from winsound import PlaySound, SND_ASYNC

        for char in self.display.WINDOWS_PROHIBITED_CHAR:
            if char in name_modified:
                self.statusbar.lbl_alert.config(
                    text=self.display.STATUSBAR["alert"])
                PlaySound("SystemAsterisk", SND_ASYNC)
                self.activate_button(False)
                break
            else:
                self.statusbar.lbl_alert.config(text="")
                self.activate_button()

    def arguments_callback(self, event):
        """Application of argument functions.

        Arguments:
            event {dict} -- Bind event
        """
        # pylint: disable=unused-argument

        for key, value in self.display.ARGUMENTS_DICT.items():
            if self.params.cbox_arguments.get() in value:
                self.display_treeview(key)

    def populate_options(self):
        """Filled the options menu."""
        entry = self.params.entry_filename
        for key, value in self.display.OPTIONS_DICT.items():
            self.params.menu_btn.menu.add_command(
                label=value,
                command=lambda k=key: entry.insert(entry.index(INSERT), k)
            )
        entry.insert(0, "[n]")


if __name__ == "__main__":
    root = Tk()
    app = MultipleRenaming(root)
    root.mainloop()
