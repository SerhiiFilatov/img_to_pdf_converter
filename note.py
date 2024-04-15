import customtkinter
import re

import data
from side_window_additional_settings import WindowForSettings, WindowForSplitSettings
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
        self.add("Text extraction")
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

    def create_window_split_set(self):
        """
        create a settings window
        :return:
        """
        window_for_settings = WindowForSplitSettings(self.engine)
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

        convert_label = MyLabel_1(self.tab("Convert to PDF"), text='Convert\nto PDF', height=30, width=70)
        convert_label.grid(row=2, column=1, padx=5, pady=5)

        convert_button = customtkinter.CTkButton(
            master=self.tab("Convert to PDF"), text='', image=data.transform_image_to_pdf, height=30, width=70,
            command=self.engine.convert_and_save
        )
        convert_button.grid(row=2, column=2, padx=5, pady=5)

        convert_additional_settings_button = customtkinter.CTkButton(
            master=self.tab("Convert to PDF"), text='', image=data.additional_settings_image, height=30, width=40,
            command=self.create_window
        )
        convert_additional_settings_button.grid(row=2, column=3, padx=5, pady=5)

        transform_label_image = MyLabel_1(self.tab("Convert to PDF"), text='Transform\nImage', height=30, width=70)
        transform_label_image.grid(row=3, column=1, padx=5, pady=5)

        transform_button_image = customtkinter.CTkButton(
            master=self.tab("Convert to PDF"), text='', image=data.transform_image, height=30, width=70,
            command=self.engine.convert_and_save
        )
        transform_button_image.grid(row=3, column=2, padx=5, pady=5)

        image_additional_settings_button = customtkinter.CTkButton(
            master=self.tab("Convert to PDF"), text='', image=data.additional_settings_image_2, height=30, width=40,
            command=self.create_window
        )
        image_additional_settings_button.grid(row=3, column=3, padx=5, pady=5)

    def create_split_merge_widgets(self):
        """
        widget window for downloading, merging, splitting PDF
        :return:
        """

        def call_split_func():
            self.engine.split_and_merge_pdf(start=self.engine.first_page_to_divide,
                                            stop=self.engine.last_page_to_divide)

        upload_label = customtkinter.CTkLabel(self.tab("Split or merge PDF file"),
                                              text='Download', height=30, width=70)
        upload_label.grid(row=1, column=1, padx=5, pady=5)

        upload_button = customtkinter.CTkButton(
            master=self.tab("Split or merge PDF file"), text='', image=data.upload_image, height=30, width=70,
            command=self.engine.open_file
        )
        upload_button.grid(row=1, column=2, padx=5, pady=5)

        merge_label = customtkinter.CTkLabel(self.tab("Split or merge PDF file"),
                                              text='Merge PDF', height=30, width=70)
        merge_label.grid(row=2, column=1, padx=5, pady=5)

        button_merge_pdf = customtkinter.CTkButton(
            master=self.tab("Split or merge PDF file"), text='', image=data.merge_icon, height=30, width=70,
            command=self.engine.merge_pdf
        )
        button_merge_pdf.grid(row=2, column=2, padx=5, pady=5)

        split_label = customtkinter.CTkLabel(self.tab("Split or merge PDF file"),
                                              text='Split PDF', height=30, width=70)
        split_label.grid(row=3, column=1, padx=5, pady=5)

        button_split_pdf = customtkinter.CTkButton(
            master=self.tab("Split or merge PDF file"), text='', image=data.split_icon, height=30, width=70,
            command=call_split_func
        )
        button_split_pdf.grid(row=3, column=2, padx=5, pady=5)

        split_settings_button = customtkinter.CTkButton(
            master=self.tab("Split or merge PDF file"), text='', image=data.additional_settings_image, height=30, width=40,
            command=self.create_window_split_set
        )
        split_settings_button.grid(row=3, column=3, padx=5, pady=5)