import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess
import os

def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        # Normalize path to use backslashes
        normalized_directory = os.path.normpath(directory)
        directory_var.set(normalized_directory)
        directory_label.config(text=f"Selected Directory: {normalized_directory}")

def run_download():
    youtube_link = link_entry.get().strip()
    audio_only = audio_var.get()
    filename = filename_entry.get().strip()
    output_dir = directory_var.get()

    if not youtube_link:
        messagebox.showerror("Error", "YouTube Link is required")
        return

    if not output_dir:
        messagebox.showerror("Error", "Please select a download directory")
        return

    precommand = f"{output_dir}\yt-dlp"
    command = [precommand]
    
    if audio_only == "yes":
        command.extend(["-x", "--audio-format", "mp3"])
    
    if filename:
        command.extend(["-o", f"{filename}.%(ext)s"])

    command.append(youtube_link)
    print(command)
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True, cwd=output_dir)
        messagebox.showinfo("Success", "Download completed successfully!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Download failed: {e.stderr}")
   
# Create main window
root = tk.Tk()
root.title("YouTube Downloader")
root.geometry("800x800")

# YouTube link input
tk.Label(root, text="YouTube Link:").pack(pady=5)
link_entry = tk.Entry(root, width=50)
link_entry.pack(pady=5)

# Audio only selector
tk.Label(root, text="Download Audio Only:").pack(pady=5)
audio_var = tk.StringVar(value="no")
audio_yes = tk.Radiobutton(root, text="Yes", variable=audio_var, value="yes")
audio_no = tk.Radiobutton(root, text="No", variable=audio_var, value="no")
audio_yes.pack()
audio_no.pack()

# Filename input
tk.Label(root, text="Filename (optional):").pack(pady=5)
filename_entry = tk.Entry(root, width=50)
filename_entry.pack(pady=5)

# Directory selector
tk.Label(root, text="Download Directory:").pack(pady=5)
directory_var = tk.StringVar()
directory_label = tk.Label(root, text="Selected Directory: None")
directory_label.pack(pady=5)
directory_button = tk.Button(root, text="Select Directory", command=select_directory)
directory_button.pack(pady=5)

# Download button
download_button = tk.Button(root, text="Download", command=run_download)
download_button.pack(pady=10)

# Start the application
root.mainloop()