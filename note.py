import customtkinter
from data import upload_image, transform_image, additional_settings_image_2, transform_image_to_pdf, \
    additional_settings_image, merge_icon, split_icon
from side_window_additional_settings import WindowForConvertSettings, WindowForSplitSettings
from engine import Engine
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
        self.add("Text extraction")
        self.add("Image converter")
        self.engine = Engine()
        self.image_converter_widgets()
        self.pdf_converter_widgets()

    def create_window_image_set(self):
        """
        Create a settings window for image conversion.
        """
        window_for_settings = WindowForConvertSettings(self.engine)
        window_for_settings.mainloop()

    def create_window_split_set(self):
        """
        Create a settings window for PDF splitting.
        """
        window_for_settings = WindowForSplitSettings(self.engine)
        window_for_settings.mainloop()

    def open_and_count(self):
        """
        Open files and count the number of images.
        """
        self.engine.open_file(self.number_of_images)

    def convert_and_count(self):
        """
        Convert images to PDF and update progress label.
        """
        self.engine.convert_and_save(self.progress_label)

    def split_and_merge_pdf(self):
        """
        Split and merge PDF files.
        """
        self.engine.split_and_merge_pdf(start=self.engine.first_page_to_divide, stop=self.engine.last_page_to_divide)

    def image_converter_widgets(self):
        """
        Create widgets for image conversion.
        """
        self.upload_label_image = NoteLabel(master=self.tab("Image converter"),
                                            text='Download\nimages',
                                            row=2, column=1)

        self.upload_button_image = NoteButton(master=self.tab("Image converter"),
                                              image=upload_image,
                                              command=self.open_and_count,
                                              row=2, column=2)

        self.number_of_images = NoteLabel(master=self.tab("Image converter"),
                                          text=f'0',
                                          row=2, column=4)

        self.transform_label_image = NoteLabel(master=self.tab("Image converter"),
                                               text='Transform\nImage',
                                               row=4, column=1)

        self.transform_button_image = NoteButton(master=self.tab("Image converter"),
                                                 image=transform_image,
                                                 command=None,
                                                 row=4, column=2)

        self.image_additional_settings_button = NoteButton(master=self.tab("Image converter"),
                                                           image=additional_settings_image_2,
                                                           command=self.create_window_image_set,
                                                           row=4, column=3)

        self.INFO_button = NoteButton(master=self.tab("Image converter"),
                                      text='INFO',
                                      command=self.engine.check_parameters,
                                      row=5, column=1)

    def pdf_converter_widgets(self):
        """
        Create widgets for PDF splitting and merging.
        """
        self.upload_label_pdf = NoteLabel(self.tab("Pdf converter"),
                                          text='Download',
                                          row=1, column=1)

        self.upload_button_pdf = NoteButton(master=self.tab("Pdf converter"),
                                            image=upload_image,
                                            command=self.open_and_count,
                                            row=1, column=2)

        self.number_of_images = NoteLabel(self.tab("Pdf converter"),
                                          text=f'0',
                                          row=1, column=4)

        self.convert_label_pdf = NoteLabel(self.tab("Pdf converter"),
                                           text=f'Convert\nto PDF',
                                           row=2, column=1)

        self.convert_button_pdf = NoteButton(master=self.tab("Pdf converter"),
                                             image=transform_image_to_pdf,
                                             command=self.convert_and_count,
                                             row=2, column=2)

        self.convert_additional_settings_button_pdf = NoteButton(master=self.tab("Pdf converter"),
                                                                 image=additional_settings_image,
                                                                 command=self.create_window_image_set,
                                                                 row=2, column=3)

        self.progress_label = NoteLabel(self.tab("Pdf converter"),
                                        text=f'Done 0 out of {str(len(self.engine.uploaded_files))}',
                                        row=2, column=4)

        self.merge_label = NoteLabel(self.tab("Pdf converter"),
                                     text='Merge PDF',
                                     row=3, column=1)

        self.button_merge_pdf = NoteButton(master=self.tab("Pdf converter"),
                                           image=merge_icon,
                                           command=self.engine.merge_pdf,
                                           row=3, column=2)

        self.split_label = NoteLabel(self.tab("Pdf converter"),
                                     text='Split PDF',
                                     row=4, column=1)

        self.button_split_pdf = NoteButton(master=self.tab("Pdf converter"),
                                           image=split_icon,
                                           command=self.split_and_merge_pdf,
                                           row=4, column=2)

        self.split_settings_button = NoteButton(master=self.tab("Pdf converter"),
                                                image=additional_settings_image,
                                                command=self.create_window_split_set,
                                                row=4, column=3)