from typing import List, Union, Callable
import customtkinter


class MyComboBoxButton:
    def __init__(self, root, height, width, x, y, values: List, command):
        self.combobox_button = customtkinter.CTkComboBox(
            root, justify='left', state="readonly", height=height,
            width=width, values=values, command=command
        )
        self.combobox_button.place(x=x, y=y)

    def get_value(self):
        select_value = self.combobox_button.get()
        return select_value


class MyEntryField:
    def __init__(self, root, x, y, width, height,):
        self.entry_field = customtkinter.CTkEntry(root, height=height, width=width,
                                                  justify='CENTER', placeholder_text="CTkEntry")
        self.entry_field.place(x=x, y=y)



class NoteLabel:
    def __init__(self, master, text, row, column,
                 width: int = 90,
                 height: int = 50,
                 padx: int = 5,
                 pady: int = 5):

        self.label = customtkinter.CTkLabel(
            master,
            text=text,
            width=width,
            height=height,
        )
        self.label.grid(row=row, column=column, padx=padx, pady=pady)
    def update_text(self, new_text):
        self.label.configure(text=new_text)



class NoteButton:
    def __init__(self, master, command, row, column,
                 text: str='',
                 image=None,
                 width: int = 90,
                 height: int = 50,
                 padx: int = 5,
                 pady: int = 5):

        self.button = customtkinter.CTkButton(
            master,
            text=text,
            image=image,
            command=command,
            width=width,
            height=height,
        )
        self.button.grid(row=row, column=column, padx=padx, pady=pady)



class FloatSpinbox(customtkinter.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 step_size: Union[int, float] = 1,
                 contrast_value,
                 command: Callable = None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.command = command

        self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = customtkinter.CTkButton(self, text="-", width=height-6, height=height-6,
                                                       command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = customtkinter.CTkEntry(self, width=width-(2*height), height=height-6, border_width=0)
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        self.add_button = customtkinter.CTkButton(self, text="+", width=height-6, height=height-6,
                                                  command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        # default value
        self.entry.insert(0, str(contrast_value))

    def add_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = float(self.entry.get()) + self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def subtract_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = float(self.entry.get()) - self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def get(self) -> Union[float, None]:
        try:
            return float(self.entry.get())
        except ValueError:
            return None

    def set(self, value: float):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(float(value)))