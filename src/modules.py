import configparser
import os
import sys
from datetime import datetime


class Modules:

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

    def date_formatting(self, get_date):
        """Date formatting management.

        Arguments:
           get_date {str} -- Date

        Returns:
            str -- formatted date
        """

        now = datetime.now()
        date_format = get_date
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

    def set_language(self, lng):
        config = configparser.ConfigParser()

        config.read("src/config.cfg")
        config["language"]["language"] = lng

        with open("src/config.cfg", "w") as configfile:
            config.write(configfile)

        # Restart app
        python = sys.executable
        os.execl(python, python, * sys.argv)
