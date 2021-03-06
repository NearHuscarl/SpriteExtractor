from tkinter import (
    Frame,
    Tk,
    END,
)


class Application(Frame):
    """ TKinter Application base class with some helper methods """

    def __init__(self, master):
        Frame.__init__(self, master)
        self.master: Tk = master
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    @classmethod
    def validate_number_value(cls, current_char):
        """ accept number value only """
        if current_char in '0123456789':
            return True
        return False

    def center_window(self):
        self.master.update_idletasks()

        width = self.master.winfo_width()
        height = self.master.winfo_height()

        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)

        self.master.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def to_clipboard(self, text):
        self.master.clipboard_clear()
        self.master.clipboard_append(text)
        self.master.update()  # now it stays on the clipboard after the window is closed

    def on_closing(self):
        pass  # override me

