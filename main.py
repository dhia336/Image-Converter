from PIL import Image
import customtkinter as ctk
from tkinter import messagebox
import os
from threading import Thread
# Functions
def get_dir_from_file(ch:str):
    a = ch.rfind("/")
    return ch
def get_ext_from_file(ch:str):
    a = ch.rfind(".")
    if a!= -1:
        return ch[a:].upper()
    else :
        return None
def check_all()->str:
    ch = ""
    if optionmenu_var.get() not  in ['JPEG', 'BMP','PNG', 'ICO', 'GIF']:
        return "choose an output format"
    if input_entry.get()=="" or not os.path.isfile(input_entry.get()):
        return "pls enter a valid input file"
    if (output_entry.get()=="" and check_var.get()=="off") :
        return "pls enter a valid output path 1"
    if ((not os.path.isdir(output_entry.get())) and (check_var.get()=="off")):
        return "pls enter a valid output path 2"
    if get_ext_from_file(output_entry.get())==optionmenu.get():
        return "output must not have same format as input"
    return ch
def convert_image(input:str, output:str, forma:str)->None:
    with Image.open(input) as img:
        if forma in ['JPEG', 'BMP'] and img.mode == 'RGBA':
            img = img.convert('RGB')  # Remove alpha channel
        elif forma in ['PNG', 'ICO', 'GIF'] and img.mode != 'RGBA':
            img = img.convert('RGBA')  # transparency support
        img.save(f"{output}\\ConvertedImage.{forma.lower()}", format=forma)
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
def input_btn_func():
    ch = ctk.filedialog.askopenfilename(title="File Name")
    if ch:
        input_entry.delete(0,len(input_entry.get()))
        input_entry.insert(0,ch)
input_btn = ctk.CTkButton(export_frame, text='Oringinal FIle', width=40, height=28,command=input_btn_func)
input_btn.grid(column=0, row=0,padx = (30,20),pady = 5,ipadx = 20,ipady = 5)
input_entry = ctk.CTkEntry(export_frame, placeholder_text='Path', width=300, height=28)
input_entry.grid(column=1, row=0,padx = (5,100),pady = 5)
def output_btn_func():
    ch = ctk.filedialog.askdirectory(title="Output Folder")
    if ch:
        output_entry.delete(0,len(output_entry.get()))
        output_entry.insert(0,ch)
output_btn = ctk.CTkButton(export_frame, text='Output Folder', width=40, height=28,command=output_btn_func)
output_btn.grid(column=2, row=0,padx = 5,pady = 5,ipadx = 20,ipady = 5)
output_entry = ctk.CTkEntry(export_frame, placeholder_text='Path', width=300, height=28)
output_entry.grid(column=3, row=0,padx = 5,pady = 5)
def checkbox_event():
    if check_var.get()=="on":
        output_entry.configure(state = "disabled")
        output_btn.configure(state = "disabled")
        output_entry.grid_forget()
        output_btn.grid_forget()
    else:
        output_entry.configure(state = "normal")
        output_btn.configure(state = "normal")
        output_entry.grid(column=3, row=0,padx = 5,pady = 5)
        output_btn.grid(column=2, row=0,padx = 5,pady = 5,ipadx = 20,ipady = 5)
check_var = ctk.StringVar(value='off')
checkbox = ctk.CTkCheckBox(export_frame, text='Output path same as Input', command=checkbox_event,
                                     width=100, height=24, checkbox_width=24, checkbox_height=24,
                                     variable=check_var, onvalue='on', offvalue='off',
                                     corner_radius=25,border_width=1)
checkbox.grid(column=3, row=1,padx = (0,20),pady = 5)
def convert_button_event():
    ch = check_all()
    if ch:
        messagebox.showerror("ERROR",ch)
    else:
        a = Thread(target=convert_image,args=(input_entry.get(),output_entry.get(),optionmenu_var.get()))
        a.start()
        messagebox.showinfo("Convetion","Done !")      

cnv_button = ctk.CTkButton(root, text='Convert', width=140, height=28,command=convert_button_event,font=("",18))
cnv_button.pack(pady = (20,10),ipadx = 20,ipady = 5)
if __name__=="__main__":
    main()