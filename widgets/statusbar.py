from tkinter import ttk


class StatusBar:
    """ Display a satusbar. """

    def __init__(self, *args):
        self.frm_status = ttk.Frame(*args, relief="sunken")

        self.lbl_count_files = ttk.Label(
            self.frm_status, text="2 fichier(s)")
        self.lbl_count_files.pack(fill="x")

        self.frm_status.pack(fill="x")
