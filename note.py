import customtkinter
import re

import data
from side_window_additional_settings import WindowForSettings
from widgets import MyLabel_1
from engine import Engine


class SelectionOfOptions(customtkinter.CTkTabview):
    """
    class CTkTabview consisting of two sections for working with PDF
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.add("Convert to PDF")
        self.add("Split or merge PDF file")
        self.engine = Engine()
        self.create_transformation_widgets()
        self.create_split_merge_widgets()

    def create_window(self):
        """
        create a settings window
        :return:
        """
        window_for_settings = WindowForSettings(self.engine)
        window_for_settings.mainloop()

    def create_transformation_widgets(self):
        """
        widget window for downloading and converting to PDF
        :return:
        """
        upload_label = MyLabel_1(self.tab("Convert to PDF"), text='Download\nimages', height=30, width=70)
        upload_label.grid(row=1, column=1, padx=5, pady=5)

        upload_button = customtkinter.CTkButton(
            master=self.tab("Convert to PDF"), text='', image=data.upload_image, height=30, width=70,
            command=self.engine.open_file
        )
        upload_button.grid(row=1, column=2, padx=5, pady=5)

        transform_label = MyLabel_1(self.tab("Convert to PDF"), text='Transform\nto PDF', height=30, width=70)
        transform_label.grid(row=2, column=1, padx=5, pady=5)

        transform_button = customtkinter.CTkButton(
            master=self.tab("Convert to PDF"), text='', image=data.transform_image, height=30, width=70,
            command=self.engine.convert_and_save
        )
        transform_button.grid(row=2, column=2, padx=5, pady=5)

        additional_settings_button = customtkinter.CTkButton(
            master=self.tab("Convert to PDF"), text='', image=data.additional_settings_image, height=30, width=40,
            command=self.create_window
        )
        additional_settings_button.grid(row=2, column=3, padx=5, pady=5)

    def create_split_merge_widgets(self):
        """
        widget window for downloading, merging, splitting PDF
        :return:
        """

        upload_label = customtkinter.CTkLabel(self.tab("Split or merge PDF file"),
                                              text='Download\nPDF file', height=30, width=70)
        upload_label.grid(row=1, column=1, padx=5, pady=5)

        upload_button = customtkinter.CTkButton(
            master=self.tab("Split or merge PDF file"), text='', image=data.upload_image, height=30, width=70,
            command=self.engine.open_file
        )
        upload_button.grid(row=1, column=2, padx=5, pady=5)

        button_merge_pdf = customtkinter.CTkButton(
            master=self.tab("Split or merge PDF file"), text='Merge pdf', height=30, width=70,
            command=self.engine.merge_pdf
        )
        button_merge_pdf.grid(row=2, column=1, padx=5, pady=5)

        self.split_pdf()

    def split_pdf(self):
        """
        separate function for splitting files
        :return:
        """

        def get_entry_value():
            """
            receiving user input
            :return: user input
            """
            self.engine.last_page_to_divide = stop_entry_field.get()
            self.engine.first_page_to_divide = start_entry_field.get()

        def multiple_commands():
            """

            :return: page numbers for split function
            """
            get_entry_value()
            self.engine.split_and_merge_pdf(start=self.engine.first_page_to_divide,
                                            stop=self.engine.last_page_to_divide)

        button_divide_pdf = customtkinter.CTkButton(
            master=self.tab("Split or merge PDF file"), text='Split PDF', height=30, width=70,
            command=multiple_commands
        )
        button_divide_pdf.grid(row=3, column=1, padx=5, pady=5)

        def is_valid(newval):
            """
            checking the entered value
            :param newval: user input
            :return: True or False
            """
            return re.match("^\d+$", newval) is not None

        check = (self.tab("Split or merge PDF file").register(is_valid), "%P")

        start_label = customtkinter.CTkLabel(self.tab("Split or merge PDF file"),
                                             text='From: ', height=30, width=30)
        start_label.place(x=90, y=87)

        start_entry_field = customtkinter.CTkEntry(self.tab("Split or merge PDF file"), placeholder_text=" ",
                                                   width=30, validate="key", validatecommand=check)
        start_entry_field.place(x=125, y=87)

        stop_label = customtkinter.CTkLabel(self.tab("Split or merge PDF file"), text='to: ', height=30, width=15)
        stop_label.place(x=160, y=87)

        stop_entry_field = customtkinter.CTkEntry(self.tab("Split or merge PDF file"), placeholder_text=" ",
                                                  width=30, validate="key", validatecommand=check)
        stop_entry_field.place(x=180, y=87)

        start_label = customtkinter.CTkLabel(self.tab("Split or merge PDF file"),
                                             text='pages.', height=30, width=30)
        start_label.place(x=215, y=87)

        self.one_or_more_pages(tab=self.tab("Split or merge PDF file"), x=90, y=122)

    def one_or_more_pages(self, tab, x, y):
        """
        splitting a file into whole or page-by-page
        :return:
        """

        def switch_event():
            self.engine.merge_all_pages = switch_var.get()

        switch_var = customtkinter.StringVar(value="on")
        switch = customtkinter.CTkSwitch(tab, text="Combine into one file.",
                                         command=switch_event, variable=switch_var, onvalue="on", offvalue="off")
        switch.place(x=x, y=y)