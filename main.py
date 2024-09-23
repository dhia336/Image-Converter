from PIL import Image
import customtkinter as ctk
from tkinterdnd2 import TkinterDnD, DND_FILES
# Functions
def check_all()->str:
    pass
def convert_image(input:str, output:str, format:str)->None:
    with Image.open(input) as img:

        if format in ['JPEG', 'BMP'] and img.mode == 'RGBA':
            img = img.convert('RGB')  # Remove alpha channel
        elif format in ['PNG', 'ICO', 'GIF'] and img.mode != 'RGBA':
            img = img.convert('RGBA')  # transparency support
        
        img.save(output, format=format)
# main function
def main():
    root.mainloop()
# Global variables
root = ctk.CTk()
big_title = ctk.CTkLabel(root, text='Image Converter', width=40, height=28, fg_color='transparent',font=("",35))
big_title.pack(padx = 10,pady = 20)
# output frame
outputf_frame = ctk.CTkFrame(root, width=200, height=200)
outputf_frame.pack(padx = 10,pady = 10)
outputf_label = ctk.CTkLabel(outputf_frame, text='Output Extention :', width=40, height=28, fg_color='transparent')
outputf_label.pack(padx = 10,side = ctk.LEFT)
optionmenu_var = ctk.StringVar(value='Choose Format')
optionmenu = ctk.CTkOptionMenu(outputf_frame,values=['PNG', 'JPEG','ICO','BMP','GIF','TIFF'],
                                         width=140, height=28,variable=optionmenu_var)
optionmenu.pack(padx = 10,pady = 5,side = ctk.LEFT)
# input and output
export_frame = ctk.CTkFrame(root, width=200, height=200)
export_frame.pack(padx = 10,pady = 5)
input_btn = ctk.CTkButton(export_frame, text='Input Path', width=40, height=28)
input_btn.grid(column=0, row=0,padx = (30,20),pady = 5,ipadx = 20,ipady = 5)
input_entry = ctk.CTkEntry(export_frame, placeholder_text='Path', width=140, height=28)
input_entry.grid(column=1, row=0,padx = (5,100),pady = 5)
output_btn = ctk.CTkButton(export_frame, text='Output Path', width=40, height=28)
output_btn.grid(column=2, row=0,padx = 5,pady = 5,ipadx = 20,ipady = 5)
output_entry = ctk.CTkEntry(export_frame, placeholder_text='Path', width=140, height=28)
output_entry.grid(column=3, row=0,padx = 5,pady = 5)
def checkbox_event():
    if check_var.get()=="on":
        output_entry.configure(state = "readonly")
        output_btn.configure(state = "disabled")
    else:
        output_entry.configure(state = "normal")
        output_btn.configure(state = "normal")

check_var = ctk.StringVar(value='off')
checkbox = ctk.CTkCheckBox(export_frame, text='Output path same as Input', command=checkbox_event,
                                     width=100, height=24, checkbox_width=24, checkbox_height=24,
                                     variable=check_var, onvalue='on', offvalue='off',)
checkbox.grid(column=3, row=1,padx = (0,20),pady = 5)
def convert_button_event():
    print('button pressed')

cnv_button = ctk.CTkButton(root, text='Convert', width=140, height=28,command=convert_button_event,font=("",18))
cnv_button.pack(pady = (20,10),ipadx = 20,ipady = 5)
if __name__=="__main__":
    main()