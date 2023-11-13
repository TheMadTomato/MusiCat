import yt_dlp
import platform
import shutil
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

class MusiCatApp:
    def __init__(self, root):
        # Set up root window
        self.root = root
        self.root.title("MusiCat")
        self.root.geometry("790x350")
        self.root.resizable(False, False)

        # Set up icon
        logo_path = os.path.join(".", "logo_1.png")
        self.logo = tk.PhotoImage(file=logo_path)
        self.root.iconphoto(False, self.logo)

        # Set up widgets
        self.link_label = tk.Label(root, text="Enter Youtube Link:")
        self.link_entry = tk.Entry(root, width=40)

        self.audio_var = tk.IntVar()
        self.video_var = tk.IntVar()

        self.audio_checkbox = tk.Checkbutton(root, text="Audio", variable=self.audio_var, command=self.toggle_audio)
        self.video_checkbox = tk.Checkbutton(root, text="Video", variable=self.video_var, command=self.toggle_video)

        self.audio_formats_label = tk.Label(root, text="Choose Audio Format:")
        self.audio_formats_combobox = ttk.Combobox(root, values=['MP3', 'AAC', 'OGG', 'M4A', 'WAV', 'OPUS'])
        self.audio_formats_combobox.set('None')

        self.video_formats_label = tk.Label(root, text="Choose Video Format:")
        self.video_formats_combobox = ttk.Combobox(root, values=['MP4', 'FLV', 'WEBM', '3GP'])
        self.video_formats_combobox.set('None')

        self.destination_label = tk.Label(root, text="Choose Destination:")
        self.destination_entry = tk.Entry(root, width=30)
        self.browse_button = tk.Button(root, text="Browse", command=self.browse_destination)

        self.download_button = tk.Button(root, text="Download", command=self.download)

        self.progressbar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")

        self.setup_ui()

    def setup_ui(self):
        # Set up widgets in grid
        self.link_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.link_entry.grid(row=0, column=1, columnspan=3, padx=10, pady=10, sticky="w")

        self.audio_checkbox.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.video_checkbox.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.audio_formats_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.audio_formats_combobox.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        self.video_formats_label.grid(row=2, column=2, padx=10, pady=5, sticky="w")
        self.video_formats_combobox.grid(row=2, column=3, padx=10, pady=5, sticky="w")

        self.destination_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.destination_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.browse_button.grid(row=3, column=2, padx=10, pady=5, sticky="w")

        self.download_button.grid(row=4, column=0, columnspan=4, pady=10)

        self.progressbar.grid(row=5, column=0, columnspan=4, pady=10)

    def toggle_audio(self):
        # Toggle audio formats
        if self.audio_var.get() == 1:
            self.audio_formats_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
            self.audio_formats_combobox.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        else:
            self.audio_formats_label.grid_forget()
            self.audio_formats_combobox.grid_forget()

    def toggle_video(self):
        # Toggle video formats
        if self.video_var.get() == 1:
            self.video_formats_label.grid(row=2, column=2, padx=10, pady=5, sticky="w")
            self.video_formats_combobox.grid(row=2, column=3, padx=10, pady=5, sticky="w")
        else:
            self.video_formats_label.grid_forget()
            self.video_formats_combobox.grid_forget()

    def browse_destination(self):
        # Browse for destination folder
        destination_folder = filedialog.askdirectory()
        self.destination_entry.delete(0, tk.END)
        self.destination_entry.insert(0, destination_folder)

    def download(self):
        # Download video/audio
        link = self.link_entry.get()
        audio_format = self.audio_formats_combobox.get() if self.audio_var.get() == 1 else None
        video_format = self.video_formats_combobox.get() if self.video_var.get() == 1 else None
        destination = self.destination_entry.get()

        if not link or (not audio_format and not video_format) or not destination:
            messagebox.showerror("Error", "Please fill in all the required fields.")
            return
        # Process download
        try:
            total_steps = (1 if audio_format else 0) + (1 if video_format else 0)
            current_step = 0

            if audio_format:
                self.progressbar["value"] = 0
                self.progressbar["maximum"] = 100
                self.progressbar.step(50)
                self.root.update_idletasks()

                download_audio(link, audio_format, destination)

                current_step += 1
                self.progressbar["value"] = int(current_step / total_steps * 100)
                self.root.update_idletasks()

            if video_format:
                self.progressbar["value"] = 0
                self.progressbar["maximum"] = 100
                self.progressbar.step(50)
                self.root.update_idletasks()

                download_video(link, video_format, destination)

                current_step += 1
                self.progressbar["value"] = int(current_step / total_steps * 100)
                self.root.update_idletasks()

            self.progressbar["value"] = 0
            messagebox.showinfo("Success", "Download completed successfully.")
        except Exception as e:
            self.progressbar["value"] = 0
            messagebox.showerror("Error", f"An error occurred: {e}")

def move_to_folder(file, destination, folder_name):
    # Move file to folder in destination depending on OS
    os_type = platform.system()
    if os_type in ['Windows', 'Linux', 'Darwin']:
        destination = os.path.join(destination, folder_name)
    else:
        raise RuntimeError("Unsupported operating system")

    try:
        shutil.move(file, os.path.expanduser(destination))
        print(f"Successfully moved to {folder_name} folder.")
    except Exception as e:
        print(f"Error moving file: {e}")

def download_audio(link, audio_format, destination):
    # Download audio function with yt-dlp module
    audio_format = audio_format.upper()
    with yt_dlp.YoutubeDL({'extract_audio': True, 'format': 'bestaudio', 'outtmpl': os.path.join(destination, '%(title)s.'+audio_format)}) as video:
        info_dict = video.extract_info(link, download=True)
        video_title = info_dict['title']
        print(video_title)
        video.download(link)
        print("Successfully Downloaded")
        move_to_folder(video_title+'.'+audio_format, destination, "Music")

def download_video(link, video_format, destination):
    # Download video function with yt-dlp module
    video_format = video_format.upper()
    with yt_dlp.YoutubeDL({'format': 'bestvideo+bestaudio', 'outtmpl': os.path.join(destination, '%(title)s.'+video_format)}) as video:
        info_dict = video.extract_info(link, download=True)
        video_title = info_dict['title']
        print(video_title)
        video.download(link)
        print("Successfully Downloaded")
        move_to_folder(video_title+'.'+video_format, destination, "Videos")

if __name__ == "__main__":
    root = tk.Tk()
    app = MusiCatApp(root)
    root.mainloop()
