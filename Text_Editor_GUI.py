import tkinter as tk
from tkinter import filedialog, messagebox
import logging

# File handler and stream handler setup
logger = logging.getLogger("Text_Editor_Logger")
logger.setLevel(logging.DEBUG)

if logger.hasHandlers():
    logger.handlers.clear()

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)  
stream_handler.setFormatter(formatter)

file_handler = logging.FileHandler("Text_Editor.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)


def new_file():
    try:

        text.delete(1.0, tk.END)
        logger.info("Created new file successfully.")
        
    except Exception as e:
        logger.error(f"Error creating file : {e}")

def open_file():
    try:

        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files","*.txt")])
        if file_path:
            with open(file_path,'r') as file:
                text.delete(1.0, tk.END)
                text.insert(tk.END, file.read())
                logger.info(f"Opened file : {file_path}")

    except Exception as e:
        logger.error(f"Error opening file : {e}")
        messagebox.showerror("Error","Failed to open file.")

def file_save():
    try:

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files","*.txt")])
        if file_path:
            with open(file_path,'w') as file:
                file.write(text.get(1.0, tk.END))
                logger.info(f"Saved file : {file_path}")
                messagebox.showinfo("Info", "File saved successfully.")

    except Exception as e:
        logger.error(f"Error saving file : {e}")
        messagebox.showerror("Error","Failed to save file.")

def main():
    global text
    try:

        root = tk.Tk()
        root.title("Simple Text Editor")
        root.geometry("800x600")

        menu = tk.Menu(root)
        root.config(menu=menu)
        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=new_file)
        file_menu.add_command(label="Open", command=open_file)
        file_menu.add_command(label="Save", command=file_save)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)

        text = tk.Text(root, wrap=tk.WORD, font=("Helvetica", 12), fg="blue")
        text.pack(expand=tk.YES, fill=tk.BOTH)

        logger.info("Text editor started successfully.")
        root.mainloop()

    except Exception as e:
        logger(f"Failed to launch text editor : {e}")


if __name__ == "__main__":
    main()
