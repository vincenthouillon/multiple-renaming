from tkinter import ttk

from src.display import Display


class StatusBar:
    """ Display a satusbar. """

    def __init__(self, master):
        self.display = Display()

        txt = "0 " + self.display.STATUSBAR["nb_files"] + " |"

        self.frm_status = ttk.Frame(master, relief="sunken")
        self.frm_status.pack(fill="x")

        self.row_status = ttk.Frame(self.frm_status)
        self.row_status.pack(fill="x")

        self.lbl_count_files = ttk.Label(
            self.row_status, text=txt)
        self.lbl_count_files.pack(side="left")

        self.lbl_alert = ttk.Label(
            self.row_status,
            text="",
            foreground="red",
            font=("sans-serif", 9, "bold"))
        self.lbl_alert.pack(side="left")
