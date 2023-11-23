import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import openai
import os
import docx
from pydub import AudioSegment
import tempfile


def split_audio(file_path, segment_duration_ms=900000, output_dir=None):
    """
    Splits the audio file into smaller segments.
    segment_duration_ms: Duration of each segment in milliseconds.
    output_dir: Directory where the segments will be temporarily stored.
    """
    audio = AudioSegment.from_file(file_path)
    segments = []

    for i in range(0, len(audio), segment_duration_ms):
        segment = audio[i:i + segment_duration_ms]
        if output_dir:
            segment_file_path = os.path.join(output_dir, f"segment_{i//segment_duration_ms}.mp3")
        else:
            segment_file_path = f"segment_{i//segment_duration_ms}.mp3"
        segment.export(segment_file_path, format="mp3")
        segments.append(segment_file_path)

    return segments


def transcribe_audio(file_path, language):
    print("Transcribing audio")
    """Transcribe the audio file using OpenAI's Whisper API."""
    with open(file_path, "rb") as audio_file:
        response = openai.Audio.transcribe(
            model="whisper-1",
            file=audio_file,
            language=language
        )
    print(response["text"])
    return response["text"]


def save_transcript(text, file_path, file_format):
    """Save the transcript in the desired format."""
    if file_format == 'txt' or file_format == 'md':
        with open(file_path, 'w') as file:
            file.write(text)
    elif file_format == 'docx':
        doc = docx.Document()
        doc.add_paragraph(text)
        doc.save(file_path)

# Global variable for the API key
api_key_var = tk.StringVar()

# Global variable for the message label
message_label = None

# Global variable for the file name entry
file_name_var = None

def transcribe_file():
    global message_label, api_key_var, file_name_var
    """Handle the transcription process."""

    # Set API Key
    openai.api_key = api_key_var.get()

    file_path = file_path_var.get()
    output_dir = output_folder.get()
    file_format = file_type_var.get()
    language = language_var.get().split('"')[1]

    if not file_path:
        messagebox.showerror("Error", "No file selected")
        return
    if not output_dir:
        messagebox.showerror("Error", "No output folder selected")
        return

    # Update message label and force GUI to update
    message_label.config(text="Transcribing... Please wait.")
    root.update_idletasks()

    if os.path.getsize(file_path) > 26214400:  # 25 MB
        with tempfile.TemporaryDirectory() as temp_dir:
            segment_paths = split_audio(file_path, output_dir=temp_dir)
            transcript = ""
            for segment_path in segment_paths:
                transcript += transcribe_audio(segment_path, language) + "\n"
    else:
        transcript = transcribe_audio(file_path, language)

    # Use the custom file name if provided
    file_base_name = file_name_var.get() if file_name_var.get() else "transcript"
    output_path = os.path.join(output_dir, f'{file_base_name}.{file_format}')
    save_transcript(transcript, output_path, file_format)
    
    # Update message label after transcription
    message_label.config(text="Transcription completed.")
    root.update_idletasks()  # Ensure the GUI updates the label
    messagebox.showinfo("Success", f"Transcription completed and saved as {output_path}")


def select_file():
    """Open a file dialog to select a file."""
    file_path = filedialog.askopenfilename()
    if file_path:
        file_path_var.set(file_path)


def select_output_folder():
    """Open a dialog to select an output folder."""
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_folder.set(folder_path)

# GUI Setup
root = tk.Tk()
root.title("Transcriber")
root.geometry("400x350")

# Improved layout and styling
style = ttk.Style()
style.theme_use('clam')  # You can experiment with different themes like 'alt', 'default', 'classic', 'vista'

file_path_var = tk.StringVar()
output_folder = tk.StringVar(value=os.getcwd())

# Use ttk.Button for a consistent look
open_button = ttk.Button(root, text="Open File", command=select_file)
open_button.pack(expand=True, pady=5)

# Use ttk.Button for the folder selection button as well
folder_button = ttk.Button(root, text="Select Output Folder", command=select_output_folder)
folder_button.pack(expand=True, pady=5)

# Entry field for custom file name
file_name_label = ttk.Label(root, text="File Name (optional):")
file_name_label.pack(expand=True, pady=5)
file_name_var = tk.StringVar()
file_name_entry = ttk.Entry(root, textvariable=file_name_var)
file_name_entry.pack(expand=True, pady=5)

file_types = ["txt", "docx", "md"]
file_type_var = tk.StringVar(value=file_types[0])

# Use ttk.OptionMenu for a consistent style
file_type_menu = ttk.OptionMenu(root, file_type_var, file_types[0], *file_types)
file_type_menu.pack(expand=True, pady=5)

# Dropdown menu for language selection
languages = ["English \"en\"", "French \"fr\"", "German \"de\"", "Spanish \"es\"", "Portuguese \"pt\"", "Italian \"it\"", "Dutch \"nl\"", "Swedish \"sv\""]
language_var = tk.StringVar(value=languages[0])

# Use ttk.OptionMenu for the language selection as well
language_menu = ttk.OptionMenu(root, language_var, languages[0], *languages)
language_menu.pack(expand=True, pady=5)

# Text field for OpenAI API Key
api_key_label = ttk.Label(root, text="OpenAI API Key:")
api_key_label.pack(expand=True, pady=5)
api_key_entry = ttk.Entry(root, textvariable=api_key_var)
api_key_entry.pack(expand=True, pady=5)

# Use ttk.Button for the transcribe button
transcribe_button = ttk.Button(root, text="Transcribe", command=transcribe_file)
transcribe_button.pack(expand=True, pady=5)

# ttk.Label for the message display
message_label = ttk.Label(root, text="")
message_label.pack(expand=True, pady=5)

root.mainloop()
