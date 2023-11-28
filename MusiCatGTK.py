import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

import yt_dlp
import os
import shutil

class MusiCatApp(Gtk.Window):
    def __init__(self):
        super(MusiCatApp, self).__init__(title="MusiCat")

        self.set_default_size(800, 400)
        self.connect("destroy", Gtk.main_quit)

        self.setup_ui()

    def setup_ui(self):
        # Create a Grid layout container
        grid = Gtk.Grid(column_spacing=10, row_spacing=10)
        self.add(grid)

        # Add widgets to the grid
        link_label = Gtk.Label(label="Enter Youtube Link:")
        self.link_entry = Gtk.Entry(width_chars=40)
        audio_checkbox = Gtk.CheckButton(label="Audio")
        video_checkbox = Gtk.CheckButton(label="Video")
        self.audio_formats_combobox = Gtk.ComboBoxText()
        self.audio_formats_combobox.append_text('MP3')
        self.audio_formats_combobox.append_text('AAC')
        self.audio_formats_combobox.append_text('OGG')
        self.audio_formats_combobox.append_text('M4A')
        self.audio_formats_combobox.append_text('WAV')
        self.audio_formats_combobox.append_text('OPUS')
        self.audio_formats_combobox.set_active(0)
        self.video_formats_combobox = Gtk.ComboBoxText()
        self.video_formats_combobox.append_text('MP4')
        self.video_formats_combobox.append_text('FLV')
        self.video_formats_combobox.append_text('WEBM')
        self.video_formats_combobox.append_text('3GP')
        self.video_formats_combobox.set_active(0)
        destination_label = Gtk.Label(label="Choose Destination:")
        self.destination_entry = Gtk.Entry(width_chars=30)
        browse_button = Gtk.Button(label="Browse")
        browse_button.connect("clicked", self.browse_destination)
        download_button = Gtk.Button(label="Download")
        download_button.connect("clicked", self.download)
        self.progressbar = Gtk.ProgressBar()

        # Add widgets to the grid layout
        grid.attach(link_label, 0, 0, 1, 1)
        grid.attach(self.link_entry, 1, 0, 3, 1)
        grid.attach(audio_checkbox, 0, 1, 1, 1)
        grid.attach(video_checkbox, 1, 1, 1, 1)
        grid.attach(destination_label, 0, 2, 1, 1)
        grid.attach(self.destination_entry, 1, 2, 1, 1)
        grid.attach(browse_button, 2, 2, 1, 1)
        grid.attach(download_button, 0, 3, 4, 1)
        grid.attach(self.progressbar, 0, 4, 4, 1)

    def browse_destination(self, button):
        destination_folder = self.show_folder_dialog()
        if destination_folder:
            self.destination_entry.set_text(destination_folder)

    def show_folder_dialog(self):
        dialog = Gtk.FileChooserDialog("Please choose a folder", self, Gtk.FileChooserAction.SELECT_FOLDER,
                                       ("Cancel", Gtk.ResponseType.CANCEL, "Open", Gtk.ResponseType.OK))
        dialog.set_default_response(Gtk.ResponseType.OK)

        response = dialog.run()
        folder_path = None
        if response == Gtk.ResponseType.OK:
            folder_path = dialog.get_filename()

        dialog.destroy()
        return folder_path

    def download(self, button):
        link = self.link_entry.get_text()
        audio_format = self.audio_formats_combobox.get_active_text()
        video_format = self.video_formats_combobox.get_active_text()
        destination = self.destination_entry.get_text()

        if not link or (not audio_format and not video_format) or not destination:
            self.show_message_dialog("Error", "Please fill in all the required fields.")
            return

        try:
            total_steps = (1 if audio_format else 0) + (1 if video_format else 0)
            current_step = 0

            if audio_format:
                self.progressbar.set_fraction(0.5)
                self.progressbar.set_text("Downloading audio...")
                self.download_audio(link, audio_format, destination)
                current_step += 1
                self.progressbar.set_fraction(current_step / total_steps)

            if video_format:
                self.progressbar.set_fraction(1.0)
                self.progressbar.set_text("Downloading video...")
                self.download_video(link, video_format, destination)
                current_step += 1
                self.progressbar.set_fraction(current_step / total_steps)

            self.progressbar.set_fraction(0)
            self.show_message_dialog("Success", "Download completed successfully.")
        except Exception as e:
            self.progressbar.set_fraction(0)
            self.show_message_dialog("Error", f"An error occurred: {e}")

    def show_message_dialog(self, title, message):
        dialog = Gtk.MessageDialog(parent=self, flags=0, type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.OK,
                                   message_format=message)
        dialog.set_title(title)
        dialog.run()
        dialog.destroy()

    def download_audio(self, link, audio_format, destination):
        audio_format = audio_format.upper()
        with yt_dlp.YoutubeDL({'extract_audio': True, 'format': 'bestaudio',
                               'outtmpl': os.path.join(destination, '%(title)s.' + audio_format)}) as video:
            info_dict = video.extract_info(link, download=True)
            video_title = info_dict['title']
            video.download(link)
            move_to_folder(video_title + '.' + audio_format, destination, "Music")

    def download_video(self, link, video_format, destination):
        video_format = video_format.upper()
        with yt_dlp.YoutubeDL({'format': 'bestvideo+bestaudio',
                               'outtmpl': os.path.join(destination, '%(title)s.' + video_format)}) as video:
            info_dict = video.extract_info(link, download=True)
            video_title = info_dict['title']
            video.download(link)
            move_to_folder(video_title + '.' + video_format, destination, "Videos")

def move_to_folder(file, destination, folder_name):
    os_type = os.name
    if os_type in ['posix', 'nt']:
        destination = os.path.join(destination, folder_name)
    else:
        raise RuntimeError("Unsupported operating system")

    try:
        shutil.move(file, os.path.expanduser(destination))
        print(f"Successfully moved to {folder_name} folder.")
    except Exception as e:
        print(f"Error moving file: {e}")

if __name__ == "__main__":
    app = MusiCatApp()
    app.show_all()
    Gtk.main()
