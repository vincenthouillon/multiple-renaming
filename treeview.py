from tkinter import *
from tkinter import ttk


class Treeview:
    """ Display Treeview. """

    def __init__(self, master):
        self.frm_header = ttk.Frame(master)
        self.tree = ttk.Treeview(master, columns=("old_name", "new_name"))

        self.tree.column("#0", minwidth=200)
        self.tree.column("#1", minwidth=200)

        self.tree.heading("#0", text="Ancien nom")
        self.tree.heading("#1", text="Nouveau nom")

        # INSERT FAKE DATA
        self.tree.insert("", "end", "1", text="file001.png", values=("img_001.png"))
        self.tree.insert("", "end", "2", text="file002.png", values=("img_002.png"))

        self.tree.pack(fill=X, expand=TRUE)
        self.frm_header.pack(fill=BOTH, expand=TRUE)
