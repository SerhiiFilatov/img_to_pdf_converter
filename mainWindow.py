import customtkinter

from note import SelectionOfOptions

customtkinter.set_appearance_mode('dark')


class MainWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Image converter")
        self.geometry("350x235+800+300")
        self.resizable(False, False)
        self.create_objects()

    def create_objects(self):

        tab_view = SelectionOfOptions(master=self, width=350, height=250)
        tab_view.grid(row=0, column=0, padx=1, pady=1)

    def run(self):
        self.mainloop()