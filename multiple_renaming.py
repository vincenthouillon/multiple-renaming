#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""Main program.

author: Vincent HOUILLON
"""

import os
import re
import sys
from tkinter.filedialog import askopenfilenames

from _datetime import datetime
from utils.utils import (arguments_parsing, get_human_readable_size)
from views.view import View


class MultipleRenaming:
    """Class Multiple Renaming."""

    def __init__(self):
        self.view = View(controller=self)

        self.initial_filenames = list()
        self.initial_filepath = list()
        self.changed_filenames = list()
        self.replace_filename = list()

    def open_filenames(self):
        """Open files and display the number in the status bar."""
        self.initial_filepath = askopenfilenames()
        self.initial_filenames = list()

        for basename in self.initial_filepath:
            self.initial_filenames.append(basename)

        self.changed_filenames = self.initial_filenames[:]
        self.replace_filename = self.initial_filenames[:]

        self.view.statusbar.var_nbfiles.set(len(self.initial_filenames))

        self.parse_filenames()

    def parse_filenames(self, argument=None):
        """Parse filenames and send to view.display_treeview."""
        data = list()

        for initial, changed in zip(
                self.initial_filenames, self.changed_filenames):
            date_creation = datetime.fromtimestamp(os.path.getmtime(initial))
            date_modified = datetime.fromtimestamp(os.path.getctime(initial))
            new_name, ext = os.path.splitext(os.path.basename(changed))
            name_modified = arguments_parsing(argument, new_name, ext)

            _data = dict()
            _data["old_name"] = os.path.basename(initial)
            _data["new_name"] = name_modified
            _data["size"] = get_human_readable_size(os.path.getsize(initial))
            _data["created_at"] = datetime.strftime(
                date_creation, "%Y/%m/%d %H:%M:%S")
            _data["modified_at"] = datetime.strftime(
                date_modified, "%Y/%m/%d %H:%M:%S")
            _data["location"] = os.path.abspath(initial)
            data.append(_data)

        self.view.display_treeview(data)

    def input_filename(self, P):
        """Check the content of the input widget to verify that it is valid
        with the rules of the application.

        Arguments:
            P {str} -- Value of the entry if the edit is allowed

        Returns:
            str -- Output text processed by application rules
        """
        user_input = P

        date_format, alert = self.view.get_format_date()

        if alert:
            self.view.statusbar.var_alert.set(alert)
            self.view.statusbar.update()
        else:
            self.view.statusbar.var_alert.set("")

        counter = int(self.view.params.start_sbox.get())

        if sys.platform == "win32":
            self.view.check_valid_characters_filename(user_input)

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

            try:
                if "[d]" in user_input:
                    temp_input = temp_input.replace("[d]", date_format)
                    new_path = os.path.join(dirname, temp_input + ext)
                    self.changed_filenames[index] = new_path
            except TypeError:
                pass

            if "[c]" in user_input:
                formated_counter = f"{counter:0{self.view.params.digits_sbox.get()}}"
                temp_input = temp_input.replace("[c]", formated_counter)
                new_path = os.path.join(dirname, temp_input + ext)
                self.changed_filenames[index] = new_path
                counter += int(self.view.params.step_sbox.get())

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

        self.parse_filenames(self.replace_filename)
        return True

    def search_and_replace(self, event):
        """Search and replace function.

        Arguments:
            event {dict} -- Bind event.
        """
        search_expr = self.view.params.find_entry.get()
        replace_expr = self.view.params.replace_entry.get()

        if sys.platform == "win32":
            self.view.check_valid_characters_filename(replace_expr)

        if len(search_expr) > 0:
            self.changed_filenames = self.replace_filename[:]
            for index, word in enumerate(self.replace_filename):
                _dirname = os.path.dirname(word)
                _basename = os.path.basename(word)

                if search_expr in word:
                    self.changed_filenames[index] = os.path.join(
                        _dirname, _basename.replace(search_expr, replace_expr))
        else:
            self.changed_filenames = self.replace_filename[:]
        self.parse_filenames(self.changed_filenames)

    def rename(self):
        """Execute file renaming."""
        for index, (initial, modified) in enumerate(zip(self.initial_filenames,
                                                        self.changed_filenames)):
            dirname = os.path.dirname(initial)
            basename_initial = os.path.basename(initial)
            extension_initial = os.path.splitext(basename_initial)[1]
            for key, value in self.view.arguments_dict.items():
                if self.view.params.arguments_cbox.get() in value:
                    arg_key = key

            # Apply argument options
            modified = arguments_parsing(arg_key,
                                         os.path.splitext(modified)[0],
                                         extension_initial)

            os.rename(initial, os.path.join(dirname, modified))

            # Convert tuple to list.
            self.initial_filenames = list(
                self.initial_filenames)

            # Update renamed file
            self.initial_filenames[index] = os.path.join(
                dirname, modified)

        self.parse_filenames()
        self.view.params.filename_entry.focus()

        if self.view.params.close_var.get():
            sys.exit()


if __name__ == "__main__":
    app = MultipleRenaming()
    app.view.main()
