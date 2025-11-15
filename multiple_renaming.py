"""
Rename several allows you to change the names of several
files at the same time. It allows you to replace the file name,
add the date, number a series of files, etc. with immediate preview
before applying changes.

author: Vincent HOUILLON
"""

import os
import sys
from tkinter.filedialog import askopenfilenames

from datetime import datetime
from utils.parser import Parser
from utils.utils import arguments_parsing, get_human_readable_size
from views.view import View


class MultipleRenaming:

    def __init__(self):
        self.view = View(controller=self)
        self.parser = Parser

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

        self.populate_treeview()

    def populate_treeview(self, argument=None):
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
        - P (str): Value of the entry if the edit is allowed

        Returns:
        - str: Output text processed by application rules
        """
        user_input = P

        date_format, alert = self.view.get_format_date()

        if alert:
            self.view.statusbar.var_alert.set(alert)
            # self.view.statusbar.update()
        else:
            self.view.statusbar.var_alert.set("")

        counter = int(self.view.params.start_sbox.get())
        step = int(self.view.params.step_sbox.get())
        digits = self.view.params.digits_sbox.get()

        if sys.platform == "win32":
            self.view.check_valid_characters_filename(user_input)

        for index, initial in enumerate(self.initial_filenames):
            dirname, filename = os.path.split(initial)
            filename, ext = os.path.splitext(filename)

            self.parser = Parser(self.changed_filenames,
                                 user_input, filename, dirname)

            # Name [n]
            temp_input = self.parser.name_n(ext, index)

            # Name from first character [nX]
            temp_input = self.parser.name_truncate_x(temp_input, ext, index)

            # Name from last character [n-X]
            temp_input = self.parser.name_last_x(temp_input, ext, index)

            # Name from n character [n,X]
            temp_input = self.parser.name_start_x(temp_input, ext, index)

            # Add counter
            temp_input = self.parser.add_counter(
                temp_input, digits, counter, ext, index)
            counter += step

            # Add date
            try:
                temp_input = self.parser.add_date(
                    temp_input, date_format, ext, index)
            except TypeError:
                pass

        self.replace_filename = self.changed_filenames[:]

        self.populate_treeview(self.replace_filename)
        return True

    def search_and_replace(self, event):
        """Search and replace function.

        Arguments:
        - event (dict): Bind event.
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
        self.populate_treeview(self.changed_filenames)

    def rename(self):
        """Execute file renaming."""
        for index, (initial, modified) in enumerate(zip(
                self.initial_filenames,
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

        self.populate_treeview()
        self.view.params.filename_entry.focus()

        if self.view.params.close_var.get():
            sys.exit()


if __name__ == "__main__":
    app = MultipleRenaming()
    app.view.main()
