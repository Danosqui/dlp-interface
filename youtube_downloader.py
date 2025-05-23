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
        directory_label.config(text=f"Directorio Seleccionado: {normalized_directory}")
        # Save the directory to config file
        with open("config.txt", "w") as f:
            f.write(normalized_directory)

def run_download():
    youtube_link = link_entry.get().strip()
    audio_only = audio_var.get()
    filename = filename_entry.get().strip()
    output_dir = directory_var.get()

    if not youtube_link:
        messagebox.showerror("Error", "Se requiere un enlace de YouTube")
        return

    if not output_dir:
        messagebox.showerror("Error", "Por favor, selecciona un directorio de descarga")
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
        messagebox.showinfo("Éxito", "¡Descarga completada con éxito!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"La descarga falló: {e.stderr}")
    except FileNotFoundError:
        messagebox.showerror("Error", "yt-dlp no se encontró en el directorio seleccionado")
    except:
        messagebox.showerror("error no sabemos que paso")

# Create main window
root = tk.Tk()
root.title("Descargador de YouTube")
root.geometry("800x800")

# YouTube link input
tk.Label(root, text="Enlace de YouTube:").pack(pady=5)
link_entry = tk.Entry(root, width=50)
link_entry.pack(pady=5)

# Audio only selector
tk.Label(root, text="Descargar Solo Audio:").pack(pady=5)
audio_var = tk.StringVar(value="no")
audio_yes = tk.Radiobutton(root, text="Sí", variable=audio_var, value="yes")
audio_no = tk.Radiobutton(root, text="No", variable=audio_var, value="no")
audio_yes.pack()
audio_no.pack()

# Filename input
tk.Label(root, text="Nombre del Archivo (opcional):").pack(pady=5)
filename_entry = tk.Entry(root, width=50)
filename_entry.pack(pady=5)

# Directory selector
tk.Label(root, text="Directorio de Descarga:").pack(pady=5)
directory_var = tk.StringVar()
directory_label = tk.Label(root, text="Directorio Seleccionado: Ninguno")
directory_label.pack(pady=5)
directory_button = tk.Button(root, text="Seleccionar Directorio", command=select_directory)
directory_button.pack(pady=5)

# Load last directory from config file if it exists
if os.path.exists("config.txt"):
    with open("config.txt", "r") as f:
        saved_directory = f.read().strip()
        if os.path.isdir(saved_directory):
            normalized_directory = os.path.normpath(saved_directory)
            directory_var.set(normalized_directory)
            directory_label.config(text=f"Directorio Seleccionado: {normalized_directory}")

# Download button
download_button = tk.Button(root, text="Descargar", command=run_download)
download_button.pack(pady=10)

# Start the application
root.mainloop()