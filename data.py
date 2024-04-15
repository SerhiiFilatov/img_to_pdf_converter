import customtkinter
from PIL import Image


image_formats = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
pdf_formats = [".pdf"]

transform_image_to_pdf = customtkinter.CTkImage(
    Image.open("C:\\Users\\User\\Desktop\\image_converter\\img_dir\\transform_pdf_icon.png"),
    size=(24, 24))

upload_image = customtkinter.CTkImage(
    Image.open("C:\\Users\\User\\Desktop\\image_converter\\img_dir\\download_icon.png"),
    size=(24, 24))

additional_settings_image = customtkinter.CTkImage(
    Image.open("C:\\Users\\User\\Desktop\\image_converter\\img_dir\\settings_icon.png"),
    size=(24, 24))

additional_settings_image_2 = customtkinter.CTkImage(
    Image.open("C:\\Users\\User\\Desktop\\image_converter\\img_dir\\exchange_icon.png"),
    size=(24, 24))

split_icon = customtkinter.CTkImage(
    Image.open("C:\\Users\\User\\Desktop\\image_converter\\img_dir\\split_icon.png"),
    size=(24, 24))

merge_icon = customtkinter.CTkImage(
    Image.open("C:\\Users\\User\\Desktop\\image_converter\\img_dir\\merge_icon.png"),
    size=(24, 24))

transform_image = customtkinter.CTkImage(
    Image.open("C:\\Users\\User\\Desktop\\image_converter\\img_dir\\transform_icon.png"),
    size=(24, 24))