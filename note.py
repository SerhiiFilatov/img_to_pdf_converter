import customtkinter

import data
from engine import Engine
from side_windows import WindowForConvertSettings, WindowForSplitSettings
from widgets import NoteLabel, NoteButton


class SelectionOfOptions(customtkinter.CTkTabview):
    """
    A class representing a tab view for working with PDF, text extraction, and image conversion.
    """

    def __init__(self, master, **kwargs):
        """
        Initializes the SelectionOfOptions object.

        Args:
            master: The parent widget.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(master, **kwargs)
        self.add("Pdf converter")
        self.add("Text recognising")
        self.engine = Engine()
        self.pdf_converter_widgets()
        self.text_extraction_widgets()


    def create_window_image_set(self):
        """
        Create a settings window for image conversion.
        """
        WindowForConvertSettings(self.engine)

    def create_window_split_set(self):
        """
        Create a settings window for PDF splitting.
        """
        WindowForSplitSettings(self.engine)

    def open_and_count_pdf(self):
        """
        Open files and count the number of images.
        """
        self.engine.open_file(self.number_of_pdf)

    def convert_and_count(self):
        """
        Convert images to PDF and update progress label.
        """
        self.engine.convert_and_save(self.progress_label, self.number_of_pdf)

    def merge_pdf(self):
        """
        Merge PDF files.
        """
        self.engine.merge_pdf(self.number_of_pdf)

    def split_and_merge_pdf(self):
        """
        Split and merge PDF files.
        """
        self.engine.split_and_merge_pdf(start=self.engine.first_page_to_divide,
                                        stop=self.engine.last_page_to_divide,
                                        number_of_pdf=self.number_of_pdf)

    def optionmenu_callback(self, choice):
        self.engine.processing_level = choice

    def pdf_converter_widgets(self):
        """
        Create widgets for PDF splitting and merging.
        """

        self.upload_label_pdf = NoteLabel(self.tab("Pdf converter"),
                                          text='Download',
                                          row=1, column=1)

        self.upload_button_pdf = NoteButton(master=self.tab("Pdf converter"),
                                            image=data.upload_image,
                                            command=self.open_and_count_pdf,
                                            row=1, column=2)

        self.number_of_pdf = NoteLabel(self.tab("Pdf converter"),
                                       text=f'0',
                                       row=1, column=4)

        self.convert_label_pdf = NoteLabel(self.tab("Pdf converter"),
                                           text=f'Convert\nto PDF',
                                           row=2, column=1)

        self.convert_button_pdf = NoteButton(master=self.tab("Pdf converter"),
                                             image=data.transform_image_2,
                                             command=self.convert_and_count,
                                             row=2, column=2)

        self.convert_additional_settings_button_pdf = NoteButton(master=self.tab("Pdf converter"),
                                                                 image=data.additional_settings_image,
                                                                 command=self.create_window_image_set,
                                                                 row=2, column=3)

        self.progress_label = NoteLabel(self.tab("Pdf converter"),
                                        text=f'0 / {str(len(self.engine.uploaded_files))}',
                                        row=2, column=4)

        self.merge_label = NoteLabel(self.tab("Pdf converter"),
                                     text='Merge PDF',
                                     row=3, column=1)

        self.button_merge_pdf = NoteButton(master=self.tab("Pdf converter"),
                                           image=data.merge_icon,
                                           command=self.merge_pdf,
                                           row=3, column=2)

        self.split_label = NoteLabel(self.tab("Pdf converter"),
                                     text='Split PDF',
                                     row=4, column=1)

        self.button_split_pdf = NoteButton(master=self.tab("Pdf converter"),
                                           image=data.split_icon,
                                           command=self.split_and_merge_pdf,
                                           row=4, column=2)

        self.split_settings_button = NoteButton(master=self.tab("Pdf converter"),
                                                image=data.additional_settings_image,
                                                command=self.create_window_split_set,
                                                row=4, column=3)

    def text_extraction_widgets(self):
        def open_and_count_in_text_rec():
            """
            Open files and count the number of images.
            """
            self.engine.open_file(self.number_of_images_in_text_rec)

        self.upload_label = NoteLabel(master=self.tab("Text recognising"),
                                      text='Download PDF',
                                      row=1, column=1, pady=10)

        self.upload_button_image = NoteButton(master=self.tab("Text recognising"),
                                              image=data.upload_image,
                                              command=open_and_count_in_text_rec,
                                              row=1, column=2)

        self.number_of_images_in_text_rec = NoteLabel(master=self.tab("Text recognising"),
                                                      text=f'0',
                                                      row=1, column=3)

        self.extract_label = NoteLabel(master=self.tab("Text recognising"),
                                       text='Text recognising',
                                       row=2, column=1, pady=10)

        self.extract_button_image = NoteButton(master=self.tab("Text recognising"),
                                               image=data.text_recognise_image,
                                               command=self.engine.start_OCR,
                                               row=2, column=2)

        optionmenu_var = customtkinter.StringVar(value="Low processing")
        optionmenu = customtkinter.CTkOptionMenu(self.tab("Text recognising"),
                                                 values=["Low processing", "Medium processing", "Deep processing"],
                                                 command=self.optionmenu_callback,
                                                 variable=optionmenu_var)
        optionmenu.grid(row=2, column=3)
