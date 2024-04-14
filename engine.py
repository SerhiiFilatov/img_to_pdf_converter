import customtkinter
import imghdr
import os
import threading
from PIL import Image, ImageEnhance
from pillow_heif import register_heif_opener
from pypdf import PdfWriter, PdfReader
from tkinter import filedialog
from tkinter import messagebox

import data
register_heif_opener()


class Engine:
    def __init__(self):
        self.uploaded_files = []
        self.contrast = 1
        self.reduce_quality = 'on'
        self.first_page_to_divide = 0
        self.last_page_to_divide = 0
        self.merge_all_pages = 'on'
        self.merge_converted_files = 'off'

    def open_file(self):
        """
        :return: list of PDF file paths
        """
        input_file_path = filedialog.askopenfilenames(
            title="Select an image",
            filetypes=[("Image files", "*.png;*.jpg;*.gif;*.bmp;*.heic;*.jpeg;*.pdf"), ("All files", "*.*")]
        )

        valid_images = [file for file in input_file_path if imghdr.what(file) is not None
                        or any(file.lower().endswith(ext) for ext in data.image_formats)
                        or any(file.lower().endswith(ext) for ext in data.pdf_formats)]

        self.uploaded_files = valid_images

    def convert_and_save(self):
        """
        converting images to pdf and save in the separate thread
        :return:
        """

        if not self.uploaded_files:
            messagebox.showinfo("No Images", "No images selected.")
            return

        output_folder = filedialog.askdirectory(title="Select a folder to save converted images")

        if not output_folder:
            return

        threading.Thread(target=self.conversion_thread, args=(output_folder,)).start()

    def conversion_thread(self, output_folder):
        """
        convert images to pdf optional with low quality
        :param output_folder: folder for saving files
        :return: pdf files or merged PDF file
        """
        pdf_files_path = []

        for input_file_path in self.uploaded_files:
            img = Image.open(input_file_path)
            contrast = ImageEnhance.Contrast(img)
            enhanced_image = contrast.enhance(self.contrast)
            output_file_path = os.path.join(output_folder,
                                            f"{os.path.splitext(os.path.basename(input_file_path))[0]}."
                                            f"pdf")
            pdf_files_path.append(output_file_path)
            enhanced_image.save(output_file_path, quality=55 if self.reduce_quality == 'on' else 90)

        # merge PDF files into PDF
        if self.merge_converted_files == 'on':
            self.merge_in_one_file(path=pdf_files_path, output_folder=output_folder)

        messagebox.showinfo("Conversion Complete", "Images converted and saved successfully.")

    def merge_pdf(self):
        """
        merging PDF files
        :return: merged PDF file
        """
        merger = PdfWriter()

        if not self.uploaded_files:
            messagebox.showinfo("No Images", "No images selected.")
            return

        if not self.check_if_pdf():
            messagebox.showinfo("No PDF")
            return

        output_folder = filedialog.askdirectory(title="Select a folder to save converted images")
        if not output_folder:
            return

        output_filepath = f"{output_folder}/merged-pdf.pdf"

        for pdf in self.uploaded_files:
            merger.append(pdf)

        with open(output_filepath, 'wb') as output_file:
            merger.write(output_file)

        messagebox.showinfo("Merge Complete", f"PDF files merged and saved to {output_filepath}")

    def split_and_merge_pdf(self, start, stop):

        start = int(start) if start else 0
        stop = int(stop) if stop else 0

        if not start or not stop:
            messagebox.showinfo("Choose pages", 'Choose pages to divide')
            return

        if start > stop:
            messagebox.showinfo("Choose pages", 'The last page number must be greater than the first page number.')
            return

        if not self.check_if_pdf():
            messagebox.showinfo("No PDF", "Choose only PDF files")
            return

        if not self.uploaded_files:
            messagebox.showinfo("No PDF", "No PDF selected.")
            return

        output_folder = filedialog.askdirectory(title="Select a folder to save converted images")

        if not output_folder:
            return

        reader = PdfReader(self.uploaded_files[0])
        pdf_pages_path = []

        # separation selected pages from a PDF file
        for x in range(int(start)-1, int(stop)):
            page = reader.pages[x]
            # cleaning PDFwriter before adding page
            divider = PdfWriter()
            divider.add_page(page)
            output_path = f"{output_folder}/page_{x + 1}.pdf"
            pdf_pages_path.append(output_path)

            with open(output_path, 'wb') as output_file:
                divider.write(output_file)

        # merge selected pages into PDF
        if self.merge_all_pages == 'on':
            self.merge_in_one_file(path=pdf_pages_path, output_folder=output_folder)

    def check_if_pdf(self):
        """
        :return: check if it is PDF file
        """
        for file in self.uploaded_files:
            if file.lower().endswith(".pdf"):
                return True

    def merge_in_one_file(self, path, output_folder):

        output_filepath = f"{output_folder}/merged-pdf.pdf"
        with open(output_filepath, 'wb') as output_file:
            # cleaning PDFwriter before adding page
            merger = PdfWriter()
            for page_path in path:
                with open(page_path, 'rb') as page_file:
                    merger.append(PdfReader(page_file))
            merger.write(output_file)
        messagebox.showinfo("Merge Complete", "Merge Complete")

        for pdf_path in path:
            os.remove(pdf_path)