"""
This is a setup.py script for Multiple Renaming.

Usage (macOS):
    python3 setup.py py2app

Usage (Windows):
    setup.py build (exe without installer)
    setup.py bdist_msi ( exe and installer)
"""

import sys

from setuptools import setup

if sys.platform == "darwin":
    extra_options = dict(
        app=['multiple_renaming.py'],
        data_files=[
            ("", ["src"]),
            ("", ["icons"]),
            ("", ["locales"]),
            ("", ["widgets"])
        ],
        options={'py2app': {"iconfile": "icons/icon.icns"}},
        setup_requires=['py2app'],
    )

elif sys.platform == "win32":
    from cx_Freeze import setup, Executable

    # http://msdn.microsoft.com/en-us/library/windows/desktop/aa371847(v=vs.85).aspx
    shortcut_table = [
        ("DesktopShortcut",                   # Shortcut
         "DesktopFolder",                     # Directory_
         "Multiple Renaming",                 # Name
         "TARGETDIR",                         # Component_
         "[TARGETDIR]Multiple Renaming.exe",  # Target
         None,                                # Arguments
         None,                                # Description
         None,                                # Hotkey
         None,                                # Icon
         None,                                # IconIndex
         None,                                # ShowCmd
         'TARGETDIR'                          # WkDir
         ),
        ("StartMenuShortcut",                 # Shortcut
         "StartMenuFolder",                   # Directory_
         "Multiple Renaming",                 # Name
         "TARGETDIR",                         # Component_
         "[TARGETDIR]Multiple Renaming.exe",  # Target
         None,                                # Arguments
         None,                                # Description
         None,                                # Hotkey
         None,                                # Icon
         None,                                # IconIndex
         None,                                # ShowCmd
         'TARGETDIR'                          # WkDir
         ),
    ]

    # Now create the table dictionary
    msi_data = {"Shortcut": shortcut_table}

    # Change some default MSI options and specify the use of the above defined
    # tables
    bdist_msi_options = {'data': msi_data}

    extra_options = dict(
        options={
            "build_exe": {
                "packages": ["src", "widgets"],
                "include_files": ["icons", "locales", "config.ini"],
            },
            "bdist_msi": bdist_msi_options,
        },
        executables=[Executable("multiple_renaming.py",
                                base="Win32GUI",
                                icon="icons/icon.ico",
                                targetName="Multiple Renaming")]
    )

else:
    extra_options = dict(
        scipts=["multiple_renaming.py"]
    )

setup(
    name="Multiple Renaming",
    version="0.8",
    author="Vincent Houillon",
    description="File renaming utility",
    license="MIT",
    **extra_options
)
