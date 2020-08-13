#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""Parse user input. Called from multiple_renaming.py."""

import os
import re


class Parser:
    """Parse user input."""

    def __init__(self, changed_filenames, user_input, filename, dirname):
        self.changed_filenames = changed_filenames
        self.user_input = user_input
        self.filename = filename
        self.dirname = dirname

    def name_n(self, ext, index):
        """Relace [n] by initial filename.

        Args:
        - ext (str): File extension.
        - index (int): Index of changed_filename.

        Returns:
        - str: User input parsed.
        """
        if "[n]" in self.user_input:
            temp_input = self.user_input.replace("[n]", self.filename)
            new_path = os.path.join(self.dirname, temp_input + ext)
            self.changed_filenames[index] = new_path
        else:
            temp_input = self.user_input
            new_path = os.path.join(self.dirname, temp_input + ext)
            self.changed_filenames[index] = new_path
        return temp_input

    def name_truncate_x(self, temp_input, ext, index):
        """Name truncate of x character [nX].

        Args:
        - temp_input (str): User input.
        - ext (str): File extension.
        - index (int): Index for changed_filename.

        Returns:
        - str: User input parsed
        """
        if re.findall(r"\[n\d+\]", self.user_input):
            re_findall = re.findall(r"\[n\d+\]", self.user_input)
            position = re_findall[0][2:len(re_findall)-2]

            len_dirname = len(os.path.dirname(self.filename))

            temp_input = temp_input.replace(
                re_findall[0],
                self.filename[len_dirname:len_dirname + int(position)])

            new_filename = os.path.join(
                self.dirname + os.sep + temp_input + ext)

            self.changed_filenames[index] = new_filename
        return temp_input

    def name_last_x(self, temp_input, ext, index):
        """Name from last character [n-X]

        Args:
        - temp_input (str): User input.
        - ext (str): File extension.
        - index (int): Index for changed_filename.

        Returns:
        - str: User input parsed
        """
        if re.findall(r"\[n-\d+\]", self.user_input):
            re_findall = re.findall(r"\[n-\d+\]", self.user_input)
            position = re_findall[0][3:len(re_findall)-2]

            nchar = len(self.filename)-int(position)
            # result = [condition is false, condition is true][condition]
            nchar = [0, nchar][nchar > 0]

            temp_input = temp_input.replace(
                re_findall[0], self.filename[nchar:])

            new_filename = os.path.join(
                self.dirname + os.sep + temp_input + ext)

            self.changed_filenames[index] = new_filename
        return temp_input

    def name_start_x(self, temp_input, ext, index):
        """Name start from x character [n,X].

        Args:
        - temp_input (str): User input.
        - ext (str): File extension.
        - index (int): Index for changed_filename.

        Returns:
        - str: User input parsed
        """
        if re.findall(r"\[n,\d+\]", self.user_input):
            re_findall = re.findall(r"\[n,\d+\]", self.user_input)
            position = re_findall[0][3:len(re_findall)-2]

            len_dirname = len(os.path.dirname(self.filename))

            temp_input = temp_input.replace(
                re_findall[0], self.filename[len_dirname + int(position):])

            new_filename = os.path.join(
                self.dirname + os.sep + temp_input + ext)

            self.changed_filenames[index] = new_filename
        return temp_input

    def add_date(self, temp_input, date_format, ext, index):
        """Add date to filename.

        Args:
        - temp_input (str): User input.
        - date_format (str): Date.
        - ext (str): File extension.
        - index (int): Index for changed_filename.

        Returns:
        - str: User input parsed.
        """
        if "[d]" in self.user_input:
            temp_input = temp_input.replace("[d]", date_format)
            new_path = os.path.join(self.dirname, temp_input + ext)
            self.changed_filenames[index] = new_path
        return temp_input

    def add_counter(self, temp_input, digits, counter, ext, index):
        """Add counter in filename.

        Args:
        - temp_input (str): User input.
        - digits (int): Number of digits.
        - counter (int): Counter
        - ext (str): File extension.
        - index (int): Index for changed_filename.

        Returns:
        - str: User input parsed.
        """
        if "[c]" in self.user_input:
            formated_counter = f"{counter:0{digits}}"
            temp_input = temp_input.replace("[c]", formated_counter)
            new_path = os.path.join(self.dirname, temp_input + ext)
            self.changed_filenames[index] = new_path
        return temp_input
