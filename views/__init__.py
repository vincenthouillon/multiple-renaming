#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""Retrieves the language selected in the config.ini file and
loads the translation module."""

import gettext
import configparser

# Load and apply settings
config = configparser.ConfigParser()
config.read("config.ini")
lng = config["language"]["language"]

try:
    text = gettext.translation("multirenaming",
                               localedir="locales", languages=[lng])
    text.install()
except FileNotFoundError:
    gettext.install(None)
