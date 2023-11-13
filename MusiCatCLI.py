import yt_dlp
import platform
import shutil
import os


def move_to_music_file(file):
    os_type = platform.system()
    if os_type == 'Windows':
        destination = os.path.join("C:", "Users", "%username%", "Music")
    elif os_type == 'Linux' or os_type == 'Darwin':
        destination = os.path.join("~", "Music")
    else:
        print("Unsupported operating system")
        return

    try:
        shutil.move(file, os.path.expanduser(destination))
        print("Successfully moved to Music folder.")
    except Exception as e:
        print(f"Error moving file: {e}")
def move_to_videos_file(file):
    os_type = platform.system()
    if os_type == 'Windows':
        destination = os.path.join("C:", "Users", "%username%", "Videos")
    elif os_type == 'Linux' or os_type == 'Darwin':
        destination = os.path.join("~", "Videos")
    else:
        print("Unsupported operating system")
        return

    try:
        shutil.move(file, os.path.expanduser(destination))
        print("Successfully moved to Videos folder.")
    except Exception as e:
        print(f"Error moving file: {e}")

def pick_audio_format():
    supported_audio_formats = ['MP3', 'AAC', 'OGG', 'M4A', 'WAV', 'OPUS']
    print("Available audio formats: ", end="")
    print(", ".join(supported_audio_formats) + ".")

    while True:
        audio_format = input("Choose the wanted audio format: ").upper()
        if audio_format in supported_audio_formats:
            return audio_format
        else:
            print("Invalid audio format. Please choose from the available options.")
def download_audio(link):
    # Download youtube audio with the yt_dlp module and save it in the format picked in pick_audio_format()
    audio_format = pick_audio_format()
    with yt_dlp.YoutubeDL({'extract_audio': True, 'format': 'bestaudio', 'outtmpl': '%(title)s.'+audio_format})\
            as video:
        info_dict = video.extract_info(link, download=True)
        video_title = info_dict['title']
        print(video_title)
        video.download(link)
        print("Successfully Downloaded")
        # move the downloaded file to the music folder
        move_to_music_file(video_title+'.'+audio_format)

def pick_video_format():
    supported_video_formats = ['MP4', 'FLV', 'WEBM', '3GP']
    print("Available video formats: ", end="")
    print(", ".join(supported_video_formats) + ".")

    while True:
        video_format = input("Choose the wanted video format: ").upper()
        if video_format in supported_video_formats:
            return video_format.lower()
        else:
            print("Invalid video format. Please choose from the available options.")
def download_video(link):
    # Download youtube video with yt-dlp module
    with yt_dlp.YoutubeDL({'format': 'bestvideo+bestaudio', 'outtmpl': '%(title)s.'+pick_video_format()})\
            as video:
        info_dict = video.extract_info(link, download=True)
        video_title = info_dict['title']
        print(video_title)
        video.download(link)
        print("Successfully Downloaded")
    # Move the downloaded file to the videos folder
    move_to_videos_file(video_title+'.mp4')

def menu(choice):
    # display a menu which allow the user whether to download audio or video
    while choice == 3:
        try:
            choice = int(input("1. Download audio\n2. Download video\n3. Exit\nEnter your choice: "))
            if choice == 1:
                link = input("Enter Youtube Link: ")
                download_audio(link)
            elif choice == 2:
                link = input("Enter Youtube Link: ")
                download_video(link)
            elif choice == 3:
                print("Exiting...")
                break
            else:
                print("Invalid choice.")
        except Exception as e:
            print(f"Error: {e}")
            break


if __name__ == '__main__':
    choice = 3
    menu(choice)
