from typing import List, Union, Callable
import customtkinter



class MyComboBoxButton:
    def __init__(self, root, height, width, x, y, values: List, command):
        self.combobox_button = customtkinter.CTkComboBox(
            root, justify='left', state="readonly", height=height,
            width=width, values=values, command=command
        )
        self.combobox_button.place(x=x, y=y)

    def get_value(self, event=None):
        select_value = self.combobox_button.get()
        return select_value


class MyEntryField:
    def __init__(self, root, x, y, width, height,):
        self.entry_field = customtkinter.CTkEntry(root, height=height, width=width,
                                                  justify='CENTER', placeholder_text="CTkEntry")
        self.entry_field.place(x=x, y=y)

class MyLabel_1(customtkinter.CTkLabel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)


class MyLabel:
    def __init__(self, root, text, height, width, row, column, padx, pady):
        self.label = customtkinter.CTkLabel(
            root, text=text, height=height, width=width, fg_color='white',
            text_color='black', corner_radius=20
        )
        self.label.grid(row=row, column=column, padx=padx, pady=pady)

    def update_text(self, new_text):
        self.label.configure(text=new_text)



class MyCheckBox:
    def __init__(self, root, row, column, padx, pady, variable):
        self.checkbox = customtkinter.CTkCheckBox(root, command=None, text='',variable=variable,
                                                  onvalue=1, offvalue=0)
        self.checkbox.grid(row=row, column=column, padx=padx, pady=pady)

    def get(self) -> Union[int, None]:
        try:
            return self.checkbox.get()
        except ValueError:
            return None



class MyProgressBar:
    def __init__(self, root, x, y):
        self.progressbar = customtkinter.CTkProgressBar(
            root, orientation="horizontal", width=80, height=20, border_width=3, corner_radius=1,
            border_color='black', fg_color='black', progress_color='green', mode="determinate")
        self.progressbar.place(x=x, y=y)

    def set_value(self, val):
        self.progressbar.set(val)

    def upd(self):
        self.progressbar.update()



class FloatSpinbox(customtkinter.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 step_size: Union[int, float] = 1,
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
        self.entry.insert(0, "1.0")

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