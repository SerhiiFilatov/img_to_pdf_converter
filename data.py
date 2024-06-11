import customtkinter
from PIL import Image


image_formats = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
pdf_formats = [".pdf"]


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

transform_image_2 = customtkinter.CTkImage(
    Image.open("C:\\Users\\User\\Desktop\\image_converter\\img_dir\\convert.png"),
    size=(24, 24))

text_recognise_image = customtkinter.CTkImage(
    Image.open("C:\\Users\\User\\Desktop\\image_converter\\img_dir\\text_editor.png"),
    size=(24, 24))

wrong_path_msg = "Use correct path to the image!\n\n" \
                 "Do not use spaces, use only English letters and digits"