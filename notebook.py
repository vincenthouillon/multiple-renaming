from tkinter import *
from tkinter import ttk

class Notebook:
    def __init__(self, *args):
        print("Notebook")
        self.frame = Frame(*args)

        self.notebk = ttk.Notebook(self.frame, padding=(0,10))
        self.settings = ttk.Frame(self.notebk)
        self.profils = ttk.Frame(self.notebk)
        self.notebk.add(self.settings, text="Paramétres")
        self.notebk.add(self.profils, text="Profils")

        # SETTINGS CONTENT
        self.labelframe = ttk.LabelFrame(self.settings, text="Méthode")
        self.labelframe.pack(fill=BOTH, pady=10)

        self.row01 = ttk.Frame(self.labelframe)
        self.row01.pack(anchor=W)

        self.col01 = ttk.Frame(self.row01)
        self.col01.pack(side=LEFT)

        self.lbl_filename = ttk.Label(self.col01, text="Nom de fichier :")
        self.lbl_filename.pack(anchor=W, padx=5)
        
        self.entry_filename = ttk.Entry(self.col01, width=60)
        self.entry_filename.pack(anchor=W, side=LEFT, padx=5)

        self.col02 = ttk.Frame(self.row01)
        self.col02.pack(side=LEFT)

        self.lbl_extension = ttk.Label(self.col02, text="Extension de fichier :")
        self.lbl_extension.pack(anchor=W, padx=5)
        
        self.entry_extension = ttk.Entry(self.col02, width=20)
        self.entry_extension.pack(anchor=W, padx=5)
        
        self.row02 = ttk.Frame(self.labelframe)
        self.row02.pack(anchor=W)

        self.lbl_arguments = ttk.Label(self.row02, text="Arguments :")
        self.lbl_arguments.pack(anchor=W, padx=5)
        
        self.entry_filename = ttk.Entry(self.row02, width=60)
        self.entry_filename.pack(anchor=W, padx=5)

        # PROFILS CONTENT
        self.lbl_filename = ttk.Label(self.profils, text="PROFILS")
        self.lbl_filename.pack()

        self.notebk.pack(fill=BOTH, side=TOP)

        self.frame.pack(fill=BOTH, side=TOP)