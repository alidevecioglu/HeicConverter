import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from tkinterdnd2 import TkinterDnD, DND_FILES
from converter import convert_heic_to_jpeg, convert_heic_file
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)

class HEICConverterGUI:
    def __init__(self, master):
        self.master = master
        master.title("HEIC to JPEG Converter")
        master.geometry("400x300") # Set a default size for the window

        # Style configuration
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12), padding=10)
        style.configure("TCheckbutton", font=("Helvetica", 12), padding=5)

        self.frame = ttk.Frame(master, width=300, height=150, relief=tk.RIDGE, borderwidth=2)
        self.frame.pack(pady=20, padx=20)

        self.drop_label = ttk.Label(self.frame, text="Drag HEIC files here or click", anchor="center")
        self.drop_label.place(relx=0.5, rely=0.5, anchor="center")

        self.frame.drop_target_register(DND_FILES)
        self.frame.dnd_bind('<<Drop>>', self.drop_file)

        self.frame.bind("<Button-1>", self.browse_file)

        self.convert_button = ttk.Button(master, text="Convert", command=self.convert)
        self.convert_button.pack(pady=10)

        self.overwrite_var = tk.BooleanVar()
        self.overwrite_check = ttk.Checkbutton(master, text="Overwrite existing JPEG files", variable=self.overwrite_var)
        self.overwrite_check.pack()

        self.console_output = tk.Text(master, width=40, height=6, wrap=tk.WORD, state=tk.DISABLED)
        self.console_output.pack(pady=10, padx=10)

        self.file_path = None

    def drop_file(self, event):
        self.file_path = event.data.strip("{}")
        self.drop_label.config(text=os.path.basename(self.file_path))

    def browse_file(self, event):
        file_path = filedialog.askopenfilename(filetypes=[("HEIC Files", "*.heic"), ("All Files", "*.*")])
        if file_path:
            self.file_path = file_path
            self.drop_label.config(text=os.path.basename(self.file_path))

    def convert(self):
        if self.file_path is None:
            self.log_to_console("No file selected. Please drag or select a HEIC file.")
            return

        overwrite = self.overwrite_var.get()

        output_text = f'Converting HEIC file: {self.file_path}\n'
        self.log_to_console(output_text)

        if os.path.isfile(self.file_path):
            convert_heic_file(self.file_path, os.path.splitext(self.file_path)[0] + ".jpg", overwrite, False)
            output_text = 'Successfully converted file\n'
            messagebox.showinfo("Conversion Success", "The HEIC file was successfully converted to JPEG.")
        else:
            output_text = 'Invalid file selected.\n'

        self.log_to_console(output_text)

    def log_to_console(self, message):
        self.console_output.config(state=tk.NORMAL)
        self.console_output.insert(tk.END, message + "\n")
        self.console_output.see(tk.END)
        self.console_output.config(state=tk.DISABLED)

def main():
    root = TkinterDnD.Tk()
    gui = HEICConverterGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
