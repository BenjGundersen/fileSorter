import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, font

# Define filetypes and their extensions.
file_types = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx"],
    "Audio": [".mp3", ".wav", ".aac", ".ogg", ".flac"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi"],
    "Archives": [".zip", ".rar", ".7z"]
}

def move_file_safely(src, dst_folder):
    if not os.path.exists(src):
        print(f"Skipping missing file: {src}")
        return

    filename = os.path.basename(src)
    name, ext = os.path.splitext(filename)
    counter = 1
    new_path = os.path.join(dst_folder, filename)

    while os.path.exists(new_path):
        new_filename = f"{name} ({counter}){ext}"
        new_path = os.path.join(dst_folder, new_filename)
        counter += 1
    
    shutil.move(src, new_path)

def sort_files(folder_path):
    if not os.path.isdir(folder_path):
        messagebox("Error", "Invalid folder path.")
        return
    
    for filename in os.listdir(folder_path):
        if filename.startswith(".") or filename.endswith(".lnk"):
            continue
        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path):
            file_ext = os.path.splitext(filename)[1].lower()
            moved = False

            for folder, extensions in file_types.items():
                print(f"Checking {filename} with extension {file_ext}")
                if  file_ext in extensions:
                    target_dir = os.path.join(folder_path, folder)
                    os.makedirs(target_dir, exist_ok=True)
                    move_file_safely(file_path, target_dir)
                    moved = True
                    break

            if not moved:
                other_dir = os.path.join(folder_path, "Other")
                os.makedirs(other_dir, exist_ok=True)
                move_file_safely(file_path, other_dir)
    
    messagebox.showinfo("Done", "Files have been sorted!")

# GUI code starts here
def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_path.set(folder)

def run_sort():
    folder = folder_path.get()
    sort_files(folder)

# GUI window
root = tk.Tk()
root.title("File Sorter")
root.geometry("400x200")
root.configure(bg="#2B2B2B")

custom_font = font.Font(family="Segoe UI", size = 10)

folder_path = tk.StringVar()

# Help Menu bar
menubar = tk.Menu(root)
helpmenu = tk.Menu(menubar, tearoff = 0)
helpmenu.add_command(label="About", command=lambda: messagebox.showinfo("About File Sorter", "File Sorter v1.0\n© 2025 BFES LLC.\nBuilt using Python"))
menubar.add_cascade(label="Help", menu=helpmenu)
root.config(menu=menubar)

label = tk.Label(
    root, 
    text="Choose a folder to sort:",
    font=custom_font
)
label.pack(pady = (20, 5))

entry = tk.Entry(
    root,
    textvariable=folder_path,
    width = 40,
    font = custom_font,
    relief="flat"
)
entry.pack(pady = (0, 10))

browse_button = tk.Button(
    root, 
    text="Browse", 
    command = browse_folder,
    font=custom_font,
    bg="#3d3d3d",
    fg ="white"
)
browse_button.pack(pady = (0, 5))

sort_button = tk.Button(
    root, 
    text="Sort Files", 
    command = run_sort,
    font=custom_font,
    bg="#3d3d3d",
    fg = "white"
)
sort_button.pack(pady = (5, 15))

root.mainloop()
