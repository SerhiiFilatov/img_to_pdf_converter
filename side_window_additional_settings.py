import re

from engine import *
from widgets import FloatSpinbox, MyLabel



class WindowForSettings(customtkinter.CTkToplevel):
    def __init__(self, engine_instance):
        super().__init__()
        self.title("Additional_settings")
        self.geometry("270x200+1155+400")
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


class WindowForSplitSettings(customtkinter.CTkToplevel):
    def __init__(self, engine_instance):
        super().__init__()
        self.title("Additional_settings")
        self.geometry("250x120+1155+400")
        self.resizable(False, False)
        self.engine = engine_instance
        self.check_var = customtkinter.IntVar(value=1)
        self.create_widgets()

    def get_entry_value(self):
        """
        receiving user input
        :return: user input
        """
        self.engine.last_page_to_divide = self.stop_entry_field.get()
        self.engine.first_page_to_divide = self.start_entry_field.get()

    def create_widgets(self):
        def is_valid(newval):
            """
            checking the entered value
            :param newval: user input
            :return: True or False
            """
            return re.match("^\d+$", newval) is not None

        check = (self.register(is_valid), "%P")

        start_label = customtkinter.CTkLabel(self,
                                             text='Select from: ', height=30, width=30)
        start_label.grid(row=1, column=1, padx=2, pady=2)

        self.start_entry_field = customtkinter.CTkEntry(self, placeholder_text=" ",
                                                   width=30, validate="key", validatecommand=check)
        self.start_entry_field.grid(row=1, column=2, padx=2, pady=2)

        middle_label = customtkinter.CTkLabel(self, text='to: ', height=30, width=15)
        middle_label.grid(row=1, column=3, padx=2, pady=2)

        self.stop_entry_field = customtkinter.CTkEntry(self, placeholder_text=" ",
                                                  width=30, validate="key", validatecommand=check)
        self.stop_entry_field.grid(row=1, column=4, padx=2, pady=2)

        stop_label = customtkinter.CTkLabel(self, text='pages.', height=30, width=15)
        stop_label.grid(row=1, column=5, padx=2, pady=2)

        def switch_event():
            self.engine.merge_all_pages = switch_var.get()

        switch_var = customtkinter.StringVar(value="on")
        switch = customtkinter.CTkSwitch(self, text="Combine into one file.",
                                         command=switch_event, variable=switch_var, onvalue="on", offvalue="off")
        switch.grid(row=3, column=1, padx=2, pady=2, columnspan=4)

        self.button_upload = customtkinter.CTkButton(
            master=self, text='Apply', height=30, width=70,
            command=self.get_settings
        )
        self.button_upload.place(x=90, y=80)

    def get_settings(self):
        self.get_entry_value()
        self.destroy()