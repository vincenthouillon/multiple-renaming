#!/usr/bin/env python3
# -*- coding:utf-8 -*-


OPTIONS_DICT = {
    "[n]": _("Name [n]"),
    "[nx]": _("Name - first x characters [nx]"),
    "[n-x]": _("Name - last x characters [n-x]"),
    "[n,x]": _("Name from x [n,x]"),
    "[c]": _("Counter [c]"),
    "[d]": _("Date - current [d]"),
}

DATE_FORMAT = [
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

ARGUMENTS_DICT = {
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

WINDOWS_PROHIBITED_CHAR = [
    "<", ">", "\\", "/", ":", "*", "?", "|", "\""
]

ALERT_CHAR = _(
    "A file name cannot contain the following characters: \ /: *? \"<> |")
