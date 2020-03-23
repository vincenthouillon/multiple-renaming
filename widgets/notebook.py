from tkinter import *
from tkinter import ttk

from widgets.constants import ARGUMENTS_LIST, OPTIONS_LIST


class Notebook:
    def __init__(self, *args):
        """ Display Notebook section. """
        self.frame = Frame(*args)

        self.notebook = ttk.Notebook(self.frame, padding=(0, 10, 0, 0))
        self.settings = ttk.Frame(self.notebook)
        self.profiles = ttk.Frame(self.notebook)
        self.notebook.add(self.settings, text="Paramètres")
        self.notebook.add(self.profiles, text="Profils")

        # CONSTANTS
        ARGUMENTS = ARGUMENTS_LIST
        OPTIONS = OPTIONS_LIST

        # --- SETTINGS CONTENT
        # region: Settings
        self.method_labelframe = ttk.LabelFrame(
            self.settings, text="Méthode", padding=(0, 5))
        self.method_labelframe.pack(fill=BOTH, pady=4, padx=10)

        # region: Row 01
        self.method_row_01 = ttk.Frame(self.method_labelframe)
        self.method_row_01.pack(anchor=W, fill=X)

        self.lbl_filename = ttk.Label(
            self.method_row_01, text="Nom de fichier :")
        self.lbl_filename.pack(anchor=W, padx=5, fill=X, expand=True)
        self.entry_filename = ttk.Entry(self.method_row_01)
        self.entry_filename.pack(
            anchor=W, side=LEFT, padx=5, fill=X, expand=True)

        self.mb = ttk.Menubutton(self.method_row_01, text="⚙️")
        self.mb.pack()
        self.mb.menu = Menu(self.mb, tearoff=False)
        self.mb["menu"] = self.mb.menu

        for key, value in OPTIONS_LIST.items():
            self.mb.menu.add_command(label=key, command=getattr(
                self, value[0]), accelerator=value[1])
        # endregion: Row 01

        # Row 02
        self.method_row_02 = ttk.Frame(self.method_labelframe)
        self.method_row_02.pack(anchor=W, fill=X, expand=True)

        self.lbl_arguments = ttk.Label(self.method_row_02, text="Arguments :")
        self.lbl_arguments.pack(anchor=W, padx=5)
        self.cbox_arguments = ttk.Combobox(
            self.method_row_02, values=ARGUMENTS, state='readonly')
        self.cbox_arguments.current(0)
        self.cbox_arguments.pack(anchor=W, fill=X, padx=5)
        # endregion: Settings

        # region: Search & Replace
        self.search_labelframe = ttk.LabelFrame(
            self.settings, text="Chercher et remplacer", padding=(0, 5))
        self.search_labelframe.pack(fill=BOTH, pady=4, padx=10)

        # Row 01
        self.search_row_01 = ttk.Frame(self.search_labelframe)
        self.search_row_01.pack(anchor=W, fill=X)

        self.search_col_01 = ttk.Frame(self.search_row_01)
        self.search_col_01.pack(side=LEFT, expand=True, fill=X)

        self.lbl_search = ttk.Label(self.search_col_01, text="Recherche :")
        self.lbl_search.pack(anchor=W, padx=5, fill=X, expand=True)
        self.entry_search = ttk.Entry(self.search_col_01)
        self.entry_search.pack(
            anchor=W, side=LEFT, padx=5, fill=X, expand=True)

        # Row 02
        self.search_row_02 = ttk.Frame(self.search_labelframe)
        self.search_row_02.pack(anchor=W, fill=X)

        self.lbl_replace = ttk.Label(self.search_row_02, text="Remplacer :")
        self.lbl_replace.pack(anchor=W, padx=5, fill=X, expand=True)
        self.entry_replace = ttk.Entry(self.search_row_02)
        self.entry_replace.pack(
            anchor=W, side=LEFT, padx=5, fill=X, expand=True)
        # endregion: Search & Replace

        # --- PROFILES CONTENT
        self.lbl_filename = ttk.Label(self.profiles, text="PROFILS")
        self.lbl_filename.pack()

        self.notebook.pack(fill=BOTH, side=TOP)

        self.frame.pack(fill=BOTH, side=BOTTOM)

    def option_01(self):
        print("OPTION 01")

    def option_02(self):
        print("OPTION 02")
