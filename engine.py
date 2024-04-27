import cv2
import imghdr
import numpy as np
import os
import threading
from pathlib import Path
from PIL import Image
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
        self.remove_shadow = 'on'
        self.first_page_to_divide = 0
        self.last_page_to_divide = 0
        self.merge_all_pages = 'on'
        self.merge_converted_files = 'off'

    def open_file(self, number_of_images):
        # Создание и запуск потока для выполнения функции open_file_thread
        thread = threading.Thread(target=self.open_file_thread, args=(number_of_images, ))
        thread.start()

    def open_file_thread(self, number_of_images):
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

        # Обновление списка загруженных файлов в основном потоке
        self.uploaded_files = valid_images

        number_of_images.update_text(new_text=f'{str(len(self.uploaded_files))}')

        # Показать информационное сообщение в основном потоке
        if len(self.uploaded_files) != 0:
            messagebox.showinfo("File Selection", "Files selected successfully")

    def convert_and_save(self, progress_label):
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

        threading.Thread(target=self.conversion_thread, args=(output_folder, progress_label)).start()

    def conversion_thread(self, output_folder, progress_label):
        """
        convert images to pdf optional with low quality, without shadow
        :param output_folder: folder for saving files
        :param progress_label:
        :return: pdf files or merged PDF file
        """
        if self.check_if_pdf():
            messagebox.showinfo("No img", "Select image file only!")
            return

        pdf_files_path = []

        for input_file_path in self.uploaded_files:

            # Path of created images
            img_path = Path(output_folder) / f"{Path(input_file_path).stem}.JPEG"

            # Path of created pdf file
            pdf_path = Path(output_folder) / f"{Path(input_file_path).stem}.pdf"

            # List of paths of created pdf files
            pdf_files_path.append(pdf_path)

            progress_label.update_text(
                new_text=f'Done {str(len(pdf_files_path))} out of {str(len(self.uploaded_files))}')

            if self.remove_shadow == 'on':
                img_with_cv2 = cv2.imread(input_file_path)
                img_without_shadow = self.remove_shadow_func(img_with_cv2)
                cv2.imwrite(str(img_path),
                            img_without_shadow,
                            [int(cv2.IMWRITE_JPEG_QUALITY), 30]
                            if self.reduce_quality == 'on' else [int(cv2.IMWRITE_JPEG_QUALITY), 95])

                img_with_pil = Image.open(str(img_path))
                img_with_pil.save(str(pdf_path))
                img_path.unlink()

            else:
                pict_with_pil = Image.open(input_file_path)
                pict_with_pil.save(str(pdf_path), quality=30 if self.reduce_quality == 'on' else 95)

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
            messagebox.showinfo("No PDF", "No PDF file selected!")
            return

        if not self.check_if_pdf():
            messagebox.showinfo("No PDF", "Select PDF file only!")
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
            messagebox.showinfo("No PDF", "Select PDF file only!")
            return

        if not self.uploaded_files:
            messagebox.showinfo("No PDF", "No PDF file selected!")
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

    @staticmethod
    def merge_in_one_file(path, output_folder):

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

    @staticmethod
    def remove_shadow_func(pixel_array):
        """
        Remove shadow from photo
        :param pixel_array: numpy array with pixels
        :return: numpy array with pixels
        """
        rgb_planes = cv2.split(pixel_array)

        result_norm_planes = []

        for plane in rgb_planes:
            dilated_img = cv2.dilate(plane, np.ones((7, 7), np.uint8))
            bg_img = cv2.medianBlur(dilated_img, 21)
            diff_img = 255 - cv2.absdiff(plane, bg_img)
            norm_img = cv2.normalize(diff_img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
            result_norm_planes.append(norm_img)

        return cv2.merge(result_norm_planes)

    def check_parameters(self):
        print(
              f'reduce_quality: {self.reduce_quality}\n'
              f'remove_shadow: {self.remove_shadow}\n'
              f'merge_converted_files: {self.merge_converted_files}\n\n'
              f'first_page:{self.first_page_to_divide} last_page: {self.last_page_to_divide}\n'
              )