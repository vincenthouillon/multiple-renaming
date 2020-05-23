from tkinter import Toplevel, Label, Frame, PhotoImage
from tkinter.ttk import Separator
import webbrowser

from src.display import Display


class About:
    """Show about window."""

    def __init__(self, link):
        self.link = link
        self.display = Display()

    def _callback(self, event):
        """Open website

        Arguments:
            event {dict} -- event
        """
        return webbrowser.open_new(self.link)

    def top_level(self, version):
        """About window toplevel.

        Arguments:
            version {str} -- Application version
        """

        TOOLBAR = self.display.TOOLBAR

        self.about = Toplevel()
        self.about.resizable(False, False)
        self.about.title(TOOLBAR["about"])
        self.about.focus()

        frame = Frame(self.about)
        frame.pack(pady=20, padx=40)

        self.img = PhotoImage(file=r"./icons/small_icon.png")
        Label(frame, image=self.img).pack()

        title = Label(frame, text="Multiple Renaming", font=("sans-serif", 16))
        title.pack()

        subtitle = Label(frame, text="File renaming utility.",
                         font=("sans-serif", 12))
        subtitle.pack()

        version_text = f"Version {version}"
        version = Label(frame, text=version_text)
        version.pack()

        self.link_lbl = Label(
            frame, text=TOOLBAR["website"], fg="blue", cursor="hand2")
        self.link_lbl.pack()
        self.link_lbl.bind("<Button-1>", self._callback)

        Separator(frame, orient="horizontal").pack(fill="x", pady=10)

        license = Label(frame, text="Copyright© 2020 - Vincent Houillon",
                        font=("sans-serif", 8))
        license.pack()
