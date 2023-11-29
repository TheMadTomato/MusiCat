# YouTube Media Downloader

## Introduction

This Python script utilizes the `yt-dlp` library to download audio and video content from YouTube. The current version supports downloading audio in the OPUS, MP3, AAC, OGG, M4A, and WAV formats. As well as downloading video in the MP4, FLV, WEBM, and 3GP formats.
## Features

- Download YouTube audio and video in formats suppoted by `yt-dlp`.
- Easily customizable with `yt-dlp` options.
- Simple command-line interface for quick usage.

## Usage

1. Make sure you have Python installed on your system.
2. Install the required dependencies using the following command:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the script using the following command:
    ```bash
    python youtube_downloader.py
    ```
4. Enter the YouTube link when prompted.

## Configuration

The script uses the `yt-dlp` library, allowing you to configure various options. Modify the script as needed to customize the download behavior.

## Future Updates

- Give the GUI a theme rather than the bland default.
- Considering rebuilding the app with `PyQT` or `Kivy`.
- Improved error handling and logging.
- Fix the Progress bar.
- Continue working on CLI version.

## Notes

The `MusiCatQT` and `MusiCatGTK` are only test programs that are not quite functional. Added them to try the porgram in other gui options. mayb be supported in the future.

## Contributing

Feel free to contribute to the project by forking the repository, making improvements, and creating a pull request. Your suggestions and contributions are highly appreciated.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the developers of `yt-dlp` for providing a powerful library for working with YouTube content.

## Version

1.0.5
