from tkinter import ttk


class Treeview:
    """ Display Treeview. """

    def __init__(self, *args):
        self.pw_header = ttk.Frame(*args)
        self.tree = ttk.Treeview(self.pw_header, column=("#0", "#01"))

        self.tree.column("#0", minwidth=200)
        self.tree.column("#1", minwidth=200)
        self.tree.column("#2", minwidth=60)

        self.tree.heading("#0", text="Ancien nom", anchor="w")
        self.tree.heading("#1", text="Nouveau nom", anchor="w")
        self.tree.heading("#2", text="Taille", anchor="w")

        # INSERT FAKE DATA
        self.tree.insert("", "end", "1", text="file001.png",
                         values=("img_001.png", "250 Ko"))
        self.tree.insert("", "end", "2", text="file002.png",
                         values=("img_002.png", "250 Ko"))

        self.tree.pack(fill="both", expand=True, anchor="n")
        self.pw_header.pack(fill="both", expand=True)