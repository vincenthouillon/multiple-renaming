from tkinter import *
from tkinter import ttk

from common.constants import Content


class Parameters:
    def __init__(self, master):
        """ Display parameters section. """
        self.frame = Frame(master)
        self.content = Content()

        self.parameters = ttk.Frame(self.frame, padding=(0, 10, 0, 0))

        # CONSTANTS
        ARGUMENTS = self.content.ARGUMENTS_DICT
        OPTIONS = self.content.OPTIONS_DICT
        DATE_FORMAT = self.content.DATE_FORMAT_LIST
        PARAMS = self.content.PARAMETERS

        # --- SETTINGS CONTENT
        self.left_panel = ttk.Frame(self.parameters)
        self.left_panel.pack(side=LEFT, fill=X, expand=True)

        # region: Settings
        self.method_labelframe = ttk.LabelFrame(
            self.left_panel, text=PARAMS["method"], padding=(0, 5))
        self.method_labelframe.pack(fill=BOTH, pady=4, padx=10)

        # region: Row 01
        self.method_row_01 = ttk.Frame(self.method_labelframe)
        self.method_row_01.pack(anchor=W, fill=X)

        self.lbl_filename = ttk.Label(
            self.method_row_01, text=PARAMS["filename"])
        self.lbl_filename.pack(anchor=W, padx=5, fill=X, expand=True)
        self.entry_filename = ttk.Entry(self.method_row_01)
        self.entry_filename.pack(
            anchor=W, side=LEFT, padx=5, fill=X, expand=True)

        self.mb = ttk.Menubutton(self.method_row_01, text="⚙️")
        self.mb.pack()
        self.mb.menu = Menu(self.mb, tearoff=False)
        self.mb["menu"] = self.mb.menu
        # endregion: Row 01

        # Row 02
        self.method_row_02 = ttk.Frame(self.method_labelframe)
        self.method_row_02.pack(anchor=W, fill=X, expand=True)

        self.lbl_arguments = ttk.Label(self.method_row_02,
                                       text=PARAMS["arguments"])
        self.lbl_arguments.pack(anchor=W, padx=5)
        self.cbox_arguments = ttk.Combobox(
            self.method_row_02, value=list(ARGUMENTS.values()), state='readonly')
        self.cbox_arguments.current(0)
        self.cbox_arguments.pack(anchor=W, fill=X, padx=5)
        # endregion: Settings

        # region: Search & Replace
        self.search_labelframe = ttk.LabelFrame(
            self.left_panel, text=PARAMS["search_and_replace"], padding=(0, 5))
        self.search_labelframe.pack(fill=BOTH, pady=4, padx=10)

        # Row 01
        self.search_row_01 = ttk.Frame(self.search_labelframe)
        self.search_row_01.pack(anchor=W, fill=X)

        self.lbl_search = ttk.Label(self.search_row_01, text=PARAMS["search"])
        self.lbl_search.pack(anchor=W, padx=5, fill=X, expand=True)
        self.entry_search = ttk.Entry(self.search_row_01)
        self.entry_search.pack(
            anchor=W, side=LEFT, padx=5, fill=X, expand=True)

        # Row 02
        self.search_row_02 = ttk.Frame(self.search_labelframe)
        self.search_row_02.pack(anchor=W, fill=X)

        self.lbl_replace = ttk.Label(
            self.search_row_02, text=PARAMS["replace"])
        self.lbl_replace.pack(anchor=W, padx=5, fill=X, expand=True)
        self.entry_replace = ttk.Entry(self.search_row_02)
        self.entry_replace.pack(
            anchor=W, side=LEFT, padx=5, fill=X, expand=True)
        # endregion: Search & Replace

        # --- RIGHT PANEL
        self.right_panel = ttk.Frame(self.parameters)
        self.right_panel.pack(side=LEFT, fill=BOTH)

        # region: Counter
        self.counter_labelframe = ttk.LabelFrame(
            self.right_panel, text=PARAMS["counter"], padding=(0, 5))
        self.counter_labelframe.pack(anchor=W, pady=4, padx=10, fill=X)

        self.count_row_01 = ttk.Frame(self.counter_labelframe)
        self.lbl_start = ttk.Label(self.count_row_01, text=PARAMS["start"])
        self.lbl_start.pack(anchor=W, side=LEFT)
        self.sbox_start = ttk.Spinbox(
            self.count_row_01, from_=0, to=1000, width=6)
        self.sbox_start.insert(0, 1)
        self.sbox_start.pack(anchor=W, padx=5, side=RIGHT)
        self.count_row_01.pack(fill=X)

        self.count_row_02 = ttk.Frame(self.counter_labelframe)
        self.lbl_step = ttk.Label(self.count_row_02, text=PARAMS["step"])
        self.lbl_step.pack(anchor=W, side=LEFT)
        self.sbox_step = ttk.Spinbox(
            self.count_row_02, from_=1, to=100, width=6)
        self.sbox_step.insert(0, 1)
        self.sbox_step.pack(anchor=W, padx=5, side=RIGHT)
        self.count_row_02.pack(fill=X, pady=2)

        self.count_row_03 = ttk.Frame(self.counter_labelframe)
        self.lbl_len = ttk.Label(self.count_row_03, text=PARAMS["digits"])
        self.lbl_len.pack(side=LEFT)
        self.sbox_len = ttk.Spinbox(self.count_row_03, from_=0, to=5, width=6)
        self.sbox_len.insert(0, 2)
        self.sbox_len.pack(anchor=W, padx=5, side=RIGHT)
        self.count_row_03.pack(fill=X)
        #endregion: Counter

        # region: Date
        self.date_labelframe = ttk.LabelFrame(
            self.right_panel, text=PARAMS["timestamp"], padding=(0, 5))
        self.date_labelframe.pack(expand=True, fill=X, pady=4, padx=10)

        self.cbox_date = ttk.Combobox(self.date_labelframe, values=DATE_FORMAT)
        self.cbox_date.current(0)
        self.cbox_date.pack(anchor=W, padx=5)
        # endregion: Date

        txt_btn = txt_btn = "✔️ " + PARAMS["btn_rename"]
        self.btn_rename = ttk.Button(
            self.right_panel, text=txt_btn)
        self.btn_rename.pack(pady=12)

        self.check_var = IntVar(value=0)
        self.cbox_rename = ttk.Checkbutton(
            self.right_panel, text=PARAMS["chk_button"],
            variable=self.check_var, onvalue=1, offvalue=0)
        self.cbox_rename.pack()

        self.parameters.pack(fill=BOTH, side=TOP)
        self.frame.pack(fill=BOTH)
