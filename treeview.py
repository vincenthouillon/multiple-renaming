from tkinter import *
from tkinter import ttk


class Treeview:
    """ Display Treeview. """

    def __init__(self, *args):
        self.pw_header = Frame(*args)
        self.tree = ttk.Treeview(self.pw_header, columns=("old_name", "new_name"))

        self.tree.column("#0", minwidth=200)
        self.tree.column("#1", minwidth=200)

        self.tree.heading("#0", text="Ancien nom", anchor=W)
        self.tree.heading("#1", text="Nouveau nom", anchor=W)

        # INSERT FAKE DATA
        self.tree.insert("", "end", "1", text="file001.png", values=("img_001.png"))
        self.tree.insert("", "end", "2", text="file002.png", values=("img_002.png"))

        self.tree.pack(fill=X, expand=TRUE, anchor=N)
        self.pw_header.pack()
