# Simple GUI for OpenAI's Whisper API Transcription

This repository contains a simple Graphical User Interface (GUI) application for transcribing audio files using OpenAI's Whisper API. The application is built using Python's Tkinter library and is designed to be user-friendly and efficient for transcribing large audio files by splitting them into smaller segments.

## Features

- **File Selection**: Easily select audio files for transcription.
- **Custom Output**: Choose the output directory and set custom file names for the transcripts.
- **Multiple Formats**: Save transcripts in TXT, DOCX, or MD formats.
- **Language Selection**: Supports multiple languages for transcription.
- **OpenAI API Key Input**: Securely enter your OpenAI API key within the application.

## Installation

Before running the application, ensure you have Python installed on your system along with the following dependencies:

- Tkinter
- OpenAI
- docx
- pydub

You can install these packages using pip:

```bash
pip install openai python-docx pydub
```

## Usage

To use the application, run the `transcriber.py` script:

```bash
python transcriber.py
```

Upon launching, you'll be presented with a straightforward interface to select your audio file, output format, language, and other options.

## Building Executable

For ease of use, you can build this script into a standalone executable. This is particularly useful if you want to distribute the application to users who may not have Python installed.

### Requirements for Building Executable

- PyInstaller

Install PyInstaller using pip if you haven't already:

```bash
pip install pyinstaller
```

### Creating the Executable

To create the executable, use the following PyInstaller command:

```bash
pyinstaller --onefile --windowed --icon=transcription.ico transcriber.py
```

This command will generate a single executable file in the `dist` folder, which can be distributed and run independently of the Python environment.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check the [issues page](https://github.com/mrfidibus7/Whisper-GUI/issues) if you want to contribute.

Project Link: [https://github.com/mrfidibus7/Whisper-GUI](<your-repo-link>)
