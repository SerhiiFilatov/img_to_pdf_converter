import customtkinter
from PIL import Image


image_formats = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
pdf_formats = [".pdf"]

transform_image = customtkinter.CTkImage(
    Image.open("C:\\Users\\User\\Desktop\\image_converter\\img_dir\\transformation_icon.png"),
    size=(24, 24))

upload_image = customtkinter.CTkImage(
    Image.open("C:\\Users\\User\\Desktop\\image_converter\\img_dir\\download_icon.png"),
    size=(24, 24))

additional_settings_image = customtkinter.CTkImage(
    Image.open("C:\\Users\\User\\Desktop\\image_converter\\img_dir\\settings_icon.png"),
    size=(24, 24))