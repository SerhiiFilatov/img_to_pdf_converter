import cv2
import imghdr
import math
import numpy as np
import os
import pytesseract
import threading
from deskew import determine_skew
from pathlib import Path
from pdf2image import convert_from_path

from PIL import Image
from pillow_heif import register_heif_opener
from pypdf import PdfWriter, PdfReader
from tkinter import filedialog
from tkinter import messagebox
from tkinter import StringVar

import data

register_heif_opener()


class Engine:
    def __init__(self):
        self.uploaded_files = []
        self.contrast = 1
        self.reduce_quality = 'off'
        self.remove_shadow = 'off'
        self.processing_level = 'Low processing'
        self.first_page_to_divide = 0
        self.last_page_to_divide = 0
        self.merge_all_pages = 'on'
        self.merge_converted_files = 'off'
        self.message = StringVar()

    def open_file(self, number_of_files):
        # Создание и запуск потока для выполнения функции open_file_thread
        thread = threading.Thread(target=self.open_file_thread, args=(number_of_files, ))
        thread.start()

    def open_file_thread(self, number_of_files):
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

        self.message = str(len(self.uploaded_files))

        number_of_files.update_text(new_text=self.message)

        # Показать информационное сообщение в основном потоке
        if len(self.uploaded_files) != 0:
            messagebox.showinfo("File Selection", "Files selected successfully")

    def convert_and_save(self, progress_label, number_of_pdf):
        """
        converting images to pdf and save in the separate thread
        :return:
        """

        if not self.uploaded_files:
            messagebox.showwarning("No Images", "No images selected.")
            return

        output_folder = filedialog.askdirectory(title="Select a folder to save converted images")

        if not output_folder:
            return

        threading.Thread(target=self.convert_and_save_thread, args=(output_folder,
                                                              progress_label,
                                                              number_of_pdf)
                         ).start()

    def convert_and_save_thread(self, output_folder, progress_label, number_of_pdf):
        """
        convert images to pdf optional with low quality, without shadow
        :param output_folder: folder for saving files
        :param progress_label:
        :return: pdf files or merged PDF file
        """
        if self.check_if_pdf():
            messagebox.showwarning("No img", "Select image file only!")
            return

        # List of paths of created pdf files
        pdf_files_path = []

        for input_file_path in self.uploaded_files:

            # Path of created images
            img_path = Path(output_folder) / f"{Path(input_file_path).stem}.JPEG"

            print(output_folder)

            # Path of created pdf file
            pdf_path = Path(output_folder) / f"{Path(input_file_path).stem}.pdf"

            pdf_files_path.append(pdf_path)

            progress_label.update_text(
                new_text=f'{str(len(pdf_files_path))} / {str(len(self.uploaded_files))}')

            if self.remove_shadow == 'on':
                try:
                    img_with_cv2 = cv2.imread(input_file_path)
                    img_without_shadow = self.remove_shadow_func(img_with_cv2)
                    cv2.imwrite(str(img_path),
                                img_without_shadow,
                                [int(cv2.IMWRITE_JPEG_QUALITY), 30]
                                if self.reduce_quality == 'on' else [int(cv2.IMWRITE_JPEG_QUALITY), 95])

                    img_with_pil = Image.open(str(img_path))
                    img_with_pil.save(str(pdf_path))
                    img_path.unlink()
                except cv2.error:
                    messagebox.showerror("Wrong path", data.wrong_path_msg)
                    self.uploaded_files.clear()
                    pdf_files_path.clear()

                    number_of_pdf.update_text(new_text=f'{str(len(self.uploaded_files))}')
                    progress_label.update_text(
                        new_text=f'{str(len(pdf_files_path))} / {str(len(self.uploaded_files))}')
                    return
            else:
                pict_with_pil = Image.open(input_file_path)
                pict_with_pil.save(str(pdf_path), quality=30 if self.reduce_quality == 'on' else 95)

        # merge PDF files into PDF
        if self.merge_converted_files == 'on':
            self.merge_in_one_file(path=pdf_files_path, output_folder=output_folder)

        clear_data = messagebox.askyesno(title="Conversion Complete",
                                         detail="Do you want to delete all downloaded files?",
                                         message="Images converted and saved successfully."
                                         )
        if clear_data:
            self.uploaded_files.clear()
            pdf_files_path.clear()
            progress_label.update_text(new_text=f'{str(len(pdf_files_path))} / '
                                                f'{str(len(self.uploaded_files))}')
            number_of_pdf.update_text(new_text=f'{str(len(self.uploaded_files))}')

    def merge_pdf(self, number_of_pdf):
        """
        merging PDF files
        :return: merged PDF file
        """
        merger = PdfWriter()

        if not self.uploaded_files:
            messagebox.showwarning("No PDF", "No PDF file selected!")
            return

        if not self.check_if_pdf():
            messagebox.showwarning("No PDF", "Select PDF file only!")
            return

        output_folder = filedialog.askdirectory(title="Select a folder to save converted images")
        if not output_folder:
            return

        output_filepath = f"{output_folder}/merged_pdf.pdf"

        for pdf in self.uploaded_files:
            merger.append(pdf)

        with open(output_filepath, 'wb') as output_file:
            merger.write(output_file)

        clear_data = messagebox.askyesno(title="Merge Complete",
                                         message=f"PDF files merged and saved to {output_filepath}",
                                         detail="Do you want to delete all downloaded files?"
                                         )
        if clear_data:
            self.uploaded_files.clear()
            number_of_pdf.update_text(new_text=f'{str(len(self.uploaded_files))}')

    def split_and_merge_pdf(self, start, stop, number_of_pdf):

        start = int(start) if start else 0
        stop = int(stop) if stop else 0

        if not start or not stop:
            messagebox.showwarning("Choose pages", 'Choose pages to divide')
            return

        if start > stop:
            messagebox.showwarning("Choose pages", 'The last page number must be greater than the first page number.')
            return

        if not self.check_if_pdf():
            messagebox.showwarning("No PDF", "Select PDF file only!")
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
        try:
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

            clear_data = messagebox.askyesno(title="PDF files splited",
                                             message=f"PDF files splited",
                                             detail="Do you want to delete all downloaded files?"
                                             )
            if clear_data:
                self.uploaded_files.clear()
                number_of_pdf.update_text(new_text=f'{str(len(self.uploaded_files))}')

        except IndexError:
            messagebox.showinfo("Out of range", "Sequence index out of range")

    def check_if_pdf(self):
        """
        :return: check if it is PDF file
        """
        for file in self.uploaded_files:
            if file.lower().endswith(".pdf"):
                return True

    @staticmethod
    def merge_in_one_file(path, output_folder):

        output_filepath = f"{output_folder}/merged_pdf.pdf"
        with open(output_filepath, 'wb') as output_file:
            # cleaning PDFwriter before adding page
            merger = PdfWriter()
            for page_path in path:
                with open(page_path, 'rb') as page_file:
                    merger.append(PdfReader(page_file))
            merger.write(output_file)

        for pdf_path in path:
            os.remove(pdf_path)

    @staticmethod
    def remove_shadow_func(pixel_array: np.ndarray) -> np.ndarray:
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

    @staticmethod
    def rotate(image: np.ndarray) -> np.ndarray:
        """
        Skewed Image correction Function
        :param image: np.ndarray
        :return:
        """
        grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        angle = determine_skew(grayscale)
        background = (255, 255, 255)

        old_width, old_height = image.shape[:2]
        angle_radian = math.radians(angle)
        width = abs(np.sin(angle_radian) * old_height) + abs(np.cos(angle_radian) * old_width)
        height = abs(np.sin(angle_radian) * old_width) + abs(np.cos(angle_radian) * old_height)

        image_center = tuple(np.array(image.shape[1::-1]) / 2)
        rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
        rot_mat[1, 2] += (width - old_width) / 2
        rot_mat[0, 2] += (height - old_height) / 2
        return cv2.warpAffine(image, rot_mat, (int(round(height)), int(round(width))), borderValue=background)

    @staticmethod
    def convert_to_images(input_file):
        images = convert_from_path(input_file)
        image = images[0]
        output_file = 'PDF_image.png'
        image.save(output_file, 'PNG')

    @staticmethod
    def extract_text_from_pdf(pdf):
        reader = PdfReader(pdf)
        page = reader.pages[0]
        text = page.extract_text()
        return text

    def medium_processing(self, image) -> np.ndarray:
        cv_image = cv2.imread(image)
        rotate_image = self.rotate(cv_image)
        remove_shadow = self.remove_shadow_func(rotate_image)
        return remove_shadow

    def extract_text_from_image(self, image):
        img = Image.open(image)
        tessdata_dir_config = r'--tessdata-dir "C:\Program Files\Tesseract-OCR\tessdata"'
        custom_config = r'--oem 1 --psm 6'
        text = pytesseract.image_to_string(img, lang='ukr', config=custom_config)
        return text

    def start_OCR(self):
        output_folder = filedialog.asksaveasfilename(title="Select a folder to save converted images")
        file = f'{output_folder}.txt'
        with open(file, "w", encoding="utf-8") as output_file:
            for input_file in self.uploaded_files:
                temp_dir = Path(os.getenv('_MEIPASS', Path('.'))) / 'temp'
                temp_dir.mkdir(parents=True, exist_ok=True)
                temp_img_path = temp_dir / f"{Path(input_file).stem}.JPEG"
                try:
                    if self.processing_level == 'Medium processing':
                        processed_img = self.medium_processing(input_file)
                        cv2.imwrite(str(temp_img_path), processed_img)

                        text = self.extract_text_from_image(temp_img_path)
                        temp_img_path.unlink()
                    else:
                        text = self.extract_text_from_image(input_file)

                    output_file.write(text + '\n')

                except Exception as e:
                    print("An error occurred while writing to file:", e)
