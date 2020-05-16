import platform
from tkinter import ttk

from src.display import Display


class Treeview:
    """ Display Treeview. """

    def __init__(self, master):
        self.pw_header = ttk.Frame(master)

        self.display = Display()

        TREEVIEW = self.display.TREEVIEW

        style = ttk.Style()
        style.configure('mystyle.Treeview', highlightthickness=0, borderwidth=0)

        self.tree = ttk.Treeview(self.pw_header, column=(
            "#0", "#01", "#02", "#03", "#04", "#05"), selectmode="none", style="mystyle.Treeview")

        if platform.system() == "Darwin":
            self.tree.tag_configure("ERR", foreground="#d63031",
                                    font=("sans-serif", 12, "bold"))
        else:
            self.tree.tag_configure("ERR", foreground="#d63031",
                                    font=("sans-serif", 10, "bold italic"))

        # Scrollbar
        horizontal_scrollbar = ttk.Scrollbar(
            self.pw_header, orient="horizontal", command=self.tree.xview)
        horizontal_scrollbar.pack(side="bottom", fill="x")
        self.tree.configure(xscrollcommand=horizontal_scrollbar.set)

        self.tree.column("#0", minwidth=180)
        self.tree.column("#1", minwidth=180)
        self.tree.column("#2", minwidth=40, width=80, anchor="e")
        self.tree.column("#3", minwidth=60, width=140)
        self.tree.column("#4", minwidth=60, width=140)
        self.tree.column("#5", minwidth=60, width=300)
        self.tree.column("#6", width=1)

        self.tree.heading("#0", text=TREEVIEW["old_name"], anchor="w")
        self.tree.heading("#1", text=TREEVIEW["new_name"], anchor="w")
        self.tree.heading("#2", text=TREEVIEW["size"], anchor="w")
        self.tree.heading("#3", text=TREEVIEW["modified"], anchor="w")
        self.tree.heading("#4", text=TREEVIEW["created"], anchor="w")
        self.tree.heading("#5", text=TREEVIEW["location"], anchor="w")

        self.tree.pack(fill="both", expand=True, anchor="n")
        self.pw_header.pack(fill="both", expand=True)
