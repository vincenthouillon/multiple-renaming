"""
This is a setup.py script for Multiple Renaming.

Usage (macOS):
    python3 setup.py py2app

Usage (Windows):
    python setup.py py2exe
"""

import sys
from setuptools import setup


APP = ['multiple_renaming.py']
DATA_FILES = [
    ("", ["src"]),
    ("", ["icons"]),
    ("", ["locales"]),
    ("", ["widgets"])
]
OPTIONS = {
    "iconfile": "icons/icon.icns"
}

if sys.platform == "darwin":
    extra_options = dict(
        app=APP,
        data_files=DATA_FILES,
        options={'py2app': OPTIONS},
        setup_requires=['py2app'],
    )
elif sys.platform == "win32":
    import py2exe
    extra_options = dict(
        setup_requires=["py2exe"],
        windows=APP,
        icon = [r"icons/icon.ico"]
    )
else:
    extra_options = dict(
        scipts=APP
    )

setup(
    name="Multiple Renaming",
    version="0.8",
    author="Vincent Houillon",
    description="File renaming utility",
    license="MIT",
    **extra_options
)