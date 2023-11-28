import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QCheckBox, QComboBox, QPushButton, \
    QFileDialog, QMessageBox, QProgressBar, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon
import yt_dlp
import platform
import shutil

class MusiCatApp(QMainWindow):
    def __init__(self):
        super(MusiCatApp, self).__init__()

        # Set up main window
        self.setWindowTitle("MusiCat")
        self.setGeometry(100, 100, 790, 350)
        self.setFixedSize(790, 350)

        # Set up icon
        logo_path = os.path.join(".", "logo_1.png")
        self.setWindowIcon(QIcon(logo_path))

        # Set up widgets
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.link_label = QLabel("Enter Youtube Link:", self.central_widget)
        self.link_entry = QLineEdit(self.central_widget)

        self.audio_var = 0
        self.video_var = 0

        self.audio_checkbox = QCheckBox("Audio", self.central_widget)
        self.video_checkbox = QCheckBox("Video", self.central_widget)

        self.audio_formats_label = QLabel("Choose Audio Format:", self.central_widget)
        self.audio_formats_combobox = QComboBox(self.central_widget)
        self.audio_formats_combobox.addItems(['MP3', 'AAC', 'OGG', 'M4A', 'WAV', 'OPUS'])
        self.audio_formats_combobox.setCurrentText('None')

        self.video_formats_label = QLabel("Choose Video Format:", self.central_widget)
        self.video_formats_combobox = QComboBox(self.central_widget)
        self.video_formats_combobox.addItems(['MP4', 'FLV', 'WEBM', '3GP'])
        self.video_formats_combobox.setCurrentText('None')

        self.destination_label = QLabel("Choose Destination:", self.central_widget)
        self.destination_entry = QLineEdit(self.central_widget)
        self.browse_button = QPushButton("Browse", self.central_widget)
        self.browse_button.clicked.connect(self.browse_destination)

        self.download_button = QPushButton("Download", self.central_widget)
        self.download_button.clicked.connect(self.download)

        self.progressbar = QProgressBar(self.central_widget)
        self.progressbar.setOrientation(1)  # Vertical orientation

        self.setup_ui()

    def setup_ui(self):
        # Set up layout
        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.link_label)
        layout.addWidget(self.link_entry)
        layout.addWidget(self.audio_checkbox)
        layout.addWidget(self.video_checkbox)
        layout.addWidget(self.audio_formats_label)
        layout.addWidget(self.audio_formats_combobox)
        layout.addWidget(self.video_formats_label)
        layout.addWidget(self.video_formats_combobox)
        layout.addWidget(self.destination_label)
        layout.addWidget(self.destination_entry)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.download_button)
        layout.addWidget(self.progressbar)

    def toggle_audio(self):
        # Toggle audio formats
        if self.audio_var == 1:
            self.audio_formats_label.show()
            self.audio_formats_combobox.show()
        else:
            self.audio_formats_label.hide()
            self.audio_formats_combobox.hide()

    def toggle_video(self):
        # Toggle video formats
        if self.video_var == 1:
            self.video_formats_label.show()
            self.video_formats_combobox.show()
        else:
            self.video_formats_label.hide()
            self.video_formats_combobox.hide()

    def browse_destination(self):
        # Browse for destination folder
        destination_folder = QFileDialog.getExistingDirectory(self, "Choose Destination")
        self.destination_entry.setText(destination_folder)

    def download(self):
        # Download video/audio
        link = self.link_entry.text()
        audio_format = self.audio_formats_combobox.currentText() if self.audio_var == 1 else None
        video_format = self.video_formats_combobox.currentText() if self.video_var == 1 else None
        destination = self.destination_entry.text()

        if not link or (not audio_format and not video_format) or not destination:
            QMessageBox.critical(self, "Error", "Please fill in all the required fields.")
            return
        # Process download
        try:
            total_steps = (1 if audio_format else 0) + (1 if video_format else 0)
            current_step = 0

            if audio_format:
                self.progressbar.setValue(0)
                self.progressbar.setMaximum(100)
                self.progressbar.setValue(50)
                QApplication.processEvents()

                download_audio(link, audio_format, destination)

                current_step += 1
                self.progressbar.setValue(int(current_step / total_steps * 100))
                QApplication.processEvents()

            if video_format:
                self.progressbar.setValue(0)
                self.progressbar.setMaximum(100)
                self.progressbar.setValue(50)
                QApplication.processEvents()

                download_video(link, video_format, destination)

                current_step += 1
                self.progressbar.setValue(int(current_step / total_steps * 100))
                QApplication.processEvents()

            self.progressbar.setValue(0)
            QMessageBox.information(self, "Success", "Download completed successfully.")
        except Exception as e:
            self.progressbar.setValue(0)
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

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
    with yt_dlp.YoutubeDL({'extract_audio': True, 'format': 'bestaudio',
                           'outtmpl': os.path.join(destination, '%(title)s.' + audio_format)}) as video:
        info_dict = video.extract_info(link, download=True)
        video_title = info_dict['title']
        print(video_title)
        video.download(link)
        print("Successfully Downloaded")
        move_to_folder(video_title + '.' + audio_format, destination, "Music")

def download_video(link, video_format, destination):
    # Download video function with yt-dlp module
    video_format = video_format.upper()
    with yt_dlp.YoutubeDL({'format': 'bestvideo+bestaudio',
                           'outtmpl': os.path.join(destination, '%(title)s.' + video_format)}) as video:
        info_dict = video.extract_info(link, download=True)
        video_title = info_dict['title']
        print(video_title)
        video.download(link)
        print("Successfully Downloaded")
        move_to_folder(video_title + '.' + video_format, destination, "Videos")

if __name__ == "__main__":
    app = QApplication([])
    window = MusiCatApp()
    window.show()
    app.exec_()
