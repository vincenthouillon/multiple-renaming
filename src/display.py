#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import gettext


class Display:

    @classmethod
    def set_language(cls, lng):
        try:
            text = gettext.translation("multirenaming",
                                            localedir="locales", languages=[lng])
            text.install()
        except:
            gettext.install(None)


    def __init__(self):
        self.ARGUMENTS_DICT = {
        0: _("No change"),
        1: _("Name in lowercase"),
        2: _("Name in uppercase"),
        3: _("Extension lowercase"),
        4: _("Extension uppercase"),
        5: _("All in lowercase"),
        6: _("All in uppercase"),
        7: _("First letter of each word lowercase"),
        8: _("First letter of each word uppercase"),
    }

        self.OPTIONS_DICT = {
                "[n]"  : _("Name [n]"),
                "[nx]" : _("Name - first x characters [nx]"),
                "[n-x]": _("Name - last x characters [n-x]"),
                "[n,x]": _("Name from x [n,x]"),
                "[c]"  : _("Counter [c]"),
                "[d]"  : _("Date - current [d]"),
            }

        self.TREEVIEW = {
            "old_name": _("Old name"),
            "new_name": _("New name"),
            "size"    : _("Size"),
            "modified" : _("Date modified"),
            "created" : _("Date created"),
            "location": _("Location"),
        }

        self.TOOLBAR = {
            "open"   : _("Open"),
            "exit"   : _("Exit"),
            "file"    : _("File"),
            "website": _("Website"),
            "about"  : _("About"),
            "help"   : _("Help"),
        }

        self.PARAMETERS = {
            "method"            : _("Method"),
            "filename"           : _("File name:"),
            "arguments"         : _("Arguments:"),
            "search_and_replace": _("Search and replace"),
            "search"            : _("Search:"),
            "replace"           : _("Replace:"),
            "counter"           : _("Counter"),
            "start"             : _("Start at:"),
            "step"              : _("Step by:"),
            "digits"            : _("Digits:"),
            "timestamp"         : _("Timestamp format"),
            "btn_rename"        : _("Rename"),
            "chk_button"        : _("Close after rename"),
        }

        self.STATUSBAR = {
            "nb_files" : _("file(s)"),
            "alert"   : _("A file name cannot contain the following characters: \ /: *? \"<> |")
        }

        # CONSTANTS
        self.DATE_FORMAT_LIST = [
            "yyyymmdd",
            "yyyy-mm-dd",
            "yyyy-mm-dd hh-nn",
            "yyyy-mm-dd hh-nn-ss",
            "dd-mm-yy",
            "dd-mm-yy hh-nn",
            "dd-mm-yy hh-nn-ss",
            "mm-dd-yyyy",
            "mm-dd-yyyy hh-nn",
            "mm-dd-yyyy hh-nn-ss",
            "yyyy",
            "yy",
            "mm",
            "mmyy",
        ]

        self.WINDOWS_PROHIBITED_CHAR = [
            "<", ">", "\\", "/", ":", "*", "?", "|", "\""
        ]
