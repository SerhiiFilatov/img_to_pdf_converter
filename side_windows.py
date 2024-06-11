import customtkinter
import re


class WindowForConvertSettings(customtkinter.CTkToplevel):
    def __init__(self, engine_instance):
        super().__init__()
        self.title("Additional_settings")
        self.geometry("270x210+1255+400")
        self.resizable(False, False)
        self.engine = engine_instance
        self.check_var = customtkinter.IntVar(value=1)
        self.create_widgets()

    def create_widgets(self):

        def event_quality():
            self.engine.reduce_quality = switch_var_quality.get()

        switch_var_quality = customtkinter.StringVar(value=self.engine.reduce_quality)
        switch_quality = customtkinter.CTkSwitch(self,
                                                 text="Reduce image quality",
                                                 command=event_quality,
                                                 variable=switch_var_quality,
                                                 onvalue="on",
                                                 offvalue="off",
                                                 font=("Arial", 18)
                                                 )
        switch_quality.place(x=30, y=30)

        def remove_shadow_command():
            self.engine.remove_shadow = switch_var_shadow.get()

        switch_var_shadow = customtkinter.StringVar(value=self.engine.remove_shadow)
        switch_shadow = customtkinter.CTkSwitch(self,
                                                text="Remove shadow",
                                                command=remove_shadow_command,
                                                variable=switch_var_shadow,
                                                onvalue="on",
                                                offvalue="off",
                                                font=("Arial", 18)
                                                )
        switch_shadow.place(x=30, y=70)

        def event_combine():
            self.engine.merge_converted_files = switch_var.get()

        switch_var = customtkinter.StringVar(value=self.engine.merge_converted_files)
        switch_combine = customtkinter.CTkSwitch(self,
                                                 text="Combine into one file.",
                                                 command=event_combine,
                                                 variable=switch_var,
                                                 onvalue="on",
                                                 offvalue="off",
                                                 font=("Arial", 18)
                                                 )
        switch_combine.place(x=30, y=110)

        self.button_upload = customtkinter.CTkButton(master=self,
                                                     text='Apply',
                                                     height=30,
                                                     width=70,
                                                     command=self.get_settings
                                                     )
        self.button_upload.place(x=100, y=160)

    def get_settings(self):
        self.destroy()



class WindowForSplitSettings(customtkinter.CTkToplevel):
    def __init__(self, engine_instance):
        super().__init__()
        self.title("Additional_settings")
        self.geometry("260x150+1255+400")
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
        def is_valid(new_val):
            """
            checking the entered value
            :param new_val: user input
            :return: True or False
            """
            return re.match("^\d+$", new_val) is not None

        check = (self.register(is_valid), "%P")

        start_label = customtkinter.CTkLabel(self,
                                             text='Select from: ', height=30, width=30)
        start_label.grid(row=1, column=1, padx=3, pady=15)

        self.start_entry_field = customtkinter.CTkEntry(self, placeholder_text=" ",
                                                        width=50, validate="key",
                                                        validatecommand=check)
        self.start_entry_field.grid(row=1, column=2, padx=3, pady=15)

        middle_label = customtkinter.CTkLabel(self, text='to: ', height=30, width=15)
        middle_label.grid(row=1, column=3, padx=3, pady=15)

        self.stop_entry_field = customtkinter.CTkEntry(self, placeholder_text=" ",
                                                       width=50, validate="key",
                                                       validatecommand=check)
        self.stop_entry_field.grid(row=1, column=4, padx=3, pady=15)

        stop_label = customtkinter.CTkLabel(self, text='pages.', height=30, width=15)
        stop_label.grid(row=1, column=5, padx=3, pady=15)

        def switch_event():
            self.engine.merge_all_pages = switch_var.get()

        switch_var = customtkinter.StringVar(value="on")
        switch = customtkinter.CTkSwitch(self, text="Combine into one file.",
                                         command=switch_event, variable=switch_var, onvalue="on", offvalue="off")
        switch.place(x=40, y=65)

        self.button_upload = customtkinter.CTkButton(
            master=self, text='Apply', height=30, width=70,
            command=self.get_settings
        )
        self.button_upload.place(x=100, y=110)

    def get_settings(self):
        self.get_entry_value()
        self.destroy()