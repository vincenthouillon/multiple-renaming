"""Retrieves the language selected in the config.ini file and
loads the translation module."""

import configparser
import gettext

# Load and apply settings
config = configparser.ConfigParser()
config.read("config.ini")
lng = config["language"]["language"]

try:
    translation = gettext.translation(
        domain="multirenaming", localedir="locales", languages=[lng]
    )
    translation.install()
except FileNotFoundError:
    gettext.install("multirenaming", "locales")
    translation = gettext.NullTranslations()
