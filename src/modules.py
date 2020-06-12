import configparser
import os
import sys
from datetime import datetime

from src.display import Display


class Modules:

    def __init__(self):
        self.display = Display()

    def get_human_readable_size(self, size, precision=0):
        """Convert n bytes into a human readable string based on format.

        Arguments:
            size {float} -- File size

        Keyword Arguments:
            precision {int} -- Number of digits after the decimal point. (default: {2})

        Returns:
            str -- Size bytes converts
        """
        suffixes = ['o', 'Ko', 'Mo', 'Go', 'To']
        suffix_index = 0
        while size > 1024 and suffix_index < 4:
            suffix_index += 1  # increment the index of the suffix
            size = size/1024.0  # apply the division
        return "%.*f %s" % (precision, size, suffixes[suffix_index])

    def arguments_parsing(self, arg, new_name, ext):
        """Analysis of arguments to apply to file names.

        Arguments:
            arg {int} -- Indeex of argument
            new_name {str} -- Filename in formatted
            ext {str} -- Extension

        Returns:
            str -- Name of the formatted file with its extension
        """
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

    def date_formatting(self, format_date, date_selected):
        """Date formatting management.

        Arguments:
           format_date {str} -- Date
           date_selected {str} -- Date user input

        Returns:
            str -- formatted date
        """

        if len(date_selected) == 19:
            date_selected = datetime.strptime(date_selected, "%d/%m/%Y %H:%M:%S")
        elif len(date_selected) == 10:
                date_selected = datetime.strptime(date_selected, "%d/%m/%Y")

        try:
            if "yyyy" in format_date:
                format_date = format_date.replace(
                    "yyyy", date_selected.strftime("%Y"))
            elif "yy" in format_date:
                format_date = format_date.replace(
                    "yy", date_selected.strftime("%y"))
            if "mm" in format_date:
                format_date = format_date.replace(
                    "mm", date_selected.strftime("%m"))
            if "dd" in format_date:
                format_date = format_date.replace(
                    "dd", date_selected.strftime("%d"))
            if "hh" in format_date:
                format_date = format_date.replace(
                    "hh", date_selected.strftime("%H"))
            if "nn" in format_date:
                format_date = format_date.replace(
                    "nn", date_selected.strftime("%M"))
            if "ss" in format_date:
                format_date = format_date.replace(
                    "ss", date_selected.strftime("%S"))
            return (format_date, None)
        except:
            return (None, self.display.STATUSBAR["date_error"])

    def set_language(self, lng):
        config = configparser.ConfigParser()

        config.read("config.ini")
        config["language"]["language"] = lng

        with open("config.ini", "w") as configfile:
            config.write(configfile)

        # Restart app
        python = sys.executable
        os.execl(python, python, * sys.argv)
    
    def date_parsing(self, user_input):
        """Crop user input text and return a valid date.

        Arguments:
            user_input {str} -- Date entered by user

        Returns:
            str -- Date
        """

        try:
            return datetime.strptime(user_input, '%d/%m/%Y')
        except ValueError:
            try:
                return datetime.strptime(user_input, '%d/%m/%Y %H:%M:%S')
            except ValueError:
                return datetime.now()
