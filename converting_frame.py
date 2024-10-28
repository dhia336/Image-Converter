from PIL import Image
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import os
from threading import Thread


class PathUtilities:
    @staticmethod
    def get_dir_from_file(path: str) -> str:
        return path.rsplit("/", 1)[0]
    @staticmethod
    def get_ext_from_file(path: str) -> str:
        return path.rsplit(".", 1)[-1].upper() if "." in path else None


class ImageConverter:
    def __init__(self):
        self.supported_formats = ['JPEG', 'BMP', 'PNG', 'ICO', 'GIF']
    def convert_image(self, input_path: str, output_path: str, format: str) -> None:
        with Image.open(input_path) as img:
            if format in ['JPEG', 'BMP'] and img.mode == 'RGBA':
                img = img.convert('RGB')  
            elif format in ['PNG', 'ICO', 'GIF'] and img.mode != 'RGBA':
                img = img.convert('RGBA')  
            img.save(os.path.join(output_path, f"ConvertedImage.{format.lower()}"), format=format)
    def validate_conversion(self, input_path: str, output_path: str, selected_format: str, same_as_input: bool) -> str:
        if selected_format not in self.supported_formats:
            return "Please choose an output format."
        if not os.path.isfile(input_path):
            return "Please enter a valid input file."
        if not same_as_input and not os.path.isdir(output_path):
            return "Please enter a valid output path."
        if PathUtilities.get_ext_from_file(input_path) == selected_format:
            return "Output format must be different from input format."
        return ""


class ImageConverterFrame(ctk.CTkFrame):
    def __init__(self, parent, converter: ImageConverter):
        super().__init__(parent)
        self.converter = converter
        self.optionmenu_var = ctk.StringVar(value='Choose Format')
        self.check_var = ctk.StringVar(value='off')

        self.setup_ui()

    def setup_ui(self):
        big_title = ctk.CTkLabel(self, text='Image Converter', font=("", 35))
        big_title.pack(padx=10, pady=20)

        output_frame = ctk.CTkFrame(self)
        output_frame.pack(padx=10, pady=10)

        output_label = ctk.CTkLabel(output_frame, text='Output Extension:')
        output_label.pack(side=ctk.LEFT, padx=10)

        self.optionmenu = ctk.CTkOptionMenu(output_frame, values=self.converter.supported_formats,
                                            variable=self.optionmenu_var)
        self.optionmenu.pack(side=ctk.LEFT, padx=10)

        path_frame = ctk.CTkFrame(self)
        path_frame.pack(padx=10, pady=5)

        self.input_entry = ctk.CTkEntry(path_frame, placeholder_text='Path')
        self.input_entry.grid(row=0, column=1, padx=5, pady=5)

        input_btn = ctk.CTkButton(path_frame, text='Original File', command=self.select_input_path)
        input_btn.grid(row=0, column=0, padx=(30, 20), pady=5)

        self.output_entry = ctk.CTkEntry(path_frame, placeholder_text='Path')
        self.output_entry.grid(row=0, column=3, padx=5, pady=5)

        output_btn = ctk.CTkButton(path_frame, text='Output Folder', command=self.select_output_path)
        output_btn.grid(row=0, column=2, padx=5, pady=5)

        checkbox = ctk.CTkCheckBox(path_frame, text='Output path same as Input', command=self.toggle_output_path,
                                   variable=self.check_var, onvalue='on', offvalue='off')
        checkbox.grid(row=1, column=3, padx=(0, 20), pady=5)

        convert_button = ctk.CTkButton(self, text='Convert', font=("", 18), command=self.start_conversion)
        convert_button.pack(pady=(20, 10), ipadx=20, ipady=5)

    def toggle_output_path(self):
        if self.check_var.get() == "on":
            self.output_entry.grid_forget()
        else:
            self.output_entry.grid(row=0, column=3, padx=5, pady=5)

    def select_input_path(self):
        file_path = ctk.filedialog.askopenfilename(title="Select Image File")
        if file_path:
            self.input_entry.delete(0, len(self.input_entry.get()))
            self.input_entry.insert(0, file_path)

    def select_output_path(self):
        folder_path = ctk.filedialog.askdirectory(title="Select Output Folder")
        if folder_path:
            self.output_entry.delete(0, len(self.output_entry.get()))
            self.output_entry.insert(0, folder_path)

    def start_conversion(self):
        input_path = self.input_entry.get()
        output_path = self.output_entry.get() if self.check_var.get() == "off" else PathUtilities.get_dir_from_file(input_path)
        selected_format = self.optionmenu_var.get()

        error_msg = self.converter.validate_conversion(input_path, output_path, selected_format, self.check_var.get() == "on")
        if error_msg:
            CTkMessagebox(title="Error", message=error_msg, icon="cancel")
            return

        conversion_thread = Thread(target=self.converter.convert_image, args=(input_path, output_path, selected_format))
        conversion_thread.start()
        CTkMessagebox(title="Success", message="Conversion Complete!", icon="check")
