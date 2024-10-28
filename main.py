from converting_frame import ImageConverterFrame, ImageConverter
import customtkinter as ctk

root = ctk.CTk()
converter = ImageConverter()
frame1 = ctk.CTkFrame(root, width=200, height=200)
frame1.pack()
converter_frame = ImageConverterFrame(parent=frame1, converter=converter)
converter_frame.pack(fill="both", expand=True)
root.mainloop()