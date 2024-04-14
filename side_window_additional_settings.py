from engine import *
from widgets import FloatSpinbox, MyLabel



class WindowForSettings(customtkinter.CTkToplevel):
    def __init__(self, engine_instance):
        super().__init__()
        self.title("Additional_settings")
        self.geometry("270x200+850+570")
        self.resizable(False, False)
        self.engine_par = engine_instance
        self.check_var = customtkinter.IntVar(value=1)
        self.create_widgets()

    def create_widgets(self):

        self.label_contrast = MyLabel(self, text='Contrast', height=30, width=70, row=1, column=1, padx=10, pady=10)
        self.spinbox_contrast = FloatSpinbox(self, width=110, step_size=0.5)
        self.spinbox_contrast.grid(row=1, column=2)

        def event_quality():
            self.engine_par.reduce_quality = switch_var.get()

        switch_var = customtkinter.StringVar(value="on")
        switch = customtkinter.CTkSwitch(self, text="Reduce image quality.",
                                         command=event_quality, variable=switch_var, onvalue="on", offvalue="off")
        switch.place(x=30, y=55)

        def event_combine():
            self.engine_par.merge_converted_files = switch_var.get()

        switch_var = customtkinter.StringVar(value=self.engine_par.merge_converted_files)
        switch = customtkinter.CTkSwitch(self, text="Combine into one file.",
                                         command=event_combine, variable=switch_var, onvalue="on", offvalue="off")
        switch.place(x=30, y=85)

        self.button_upload = customtkinter.CTkButton(
            master=self, text='Apply', height=30, width=70,
            command=self.get_settings
        )
        self.button_upload.place(x=100, y=150)

    def get_settings(self):
        self.engine_par.contrast = self.spinbox_contrast.get()
        self.destroy()