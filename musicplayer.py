import tkinter as tk
from tkinter import filedialog
import pygame
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pydub import AudioSegment
from scipy.io.wavfile import write
import io

# Initialize Pygame mixer
pygame.mixer.init()

# Global variable for the current file
current_file = None

# Function to load a music file
def load_music():
    global current_file
    current_file = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav")])
    if current_file:
        if current_file.endswith('.mp3'):
            convert_mp3_to_wav(current_file)
        pygame.mixer.music.load(current_file)
        visualize_music()
        play_music()

# Function to convert mp3 to wav
def convert_mp3_to_wav(mp3_file):
    wav_file = mp3_file.rsplit('.', 1)[0] + '.wav'
    audio = AudioSegment.from_mp3(mp3_file)
    audio.export(wav_file, format="wav")
    return wav_file

# Function to play the loaded music
def play_music():
    if current_file:
        pygame.mixer.music.play()

# Function to pause the music
def pause_music():
    pygame.mixer.music.pause()

# Function to unpause the music
def unpause_music():
    pygame.mixer.music.unpause()

# Function to stop the music
def stop_music():
    pygame.mixer.music.stop()

# Function to visualize the music
def visualize_music():
    if current_file:
        if current_file.endswith('.wav'):
            sample_rate, data = wavfile.read(current_file)
        else:
            sample_rate, data = convert_mp3_to_wav(current_file)
            sample_rate, data = wavfile.read(data)
        
        # Use only one channel for simplicity
        if len(data.shape) > 1:
            data = data[:, 0]

        fig, ax = plt.subplots()
        ax.plot(data)
        ax.set_title('Waveform of the Audio File')
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)
    else:
        # If the file is not a .wav file, show a message
        error_label = tk.Label(root, text="Visualization is only supported for .wav and .mp3 files", fg="red")
        error_label.pack(pady=10)

# Create the main window
root = tk.Tk()
root.title("Python Music Player with Visualizer")

# Create buttons for control
load_button = tk.Button(root, text="Load Music", command=load_music)
play_button = tk.Button(root, text="Play", command=play_music)
pause_button = tk.Button(root, text="Pause", command=pause_music)
unpause_button = tk.Button(root, text="Unpause", command=unpause_music)
stop_button = tk.Button(root, text="Stop", command=stop_music)

# Arrange buttons in the window
load_button.pack(pady=10)
play_button.pack(pady=10)
pause_button.pack(pady=10)
unpause_button.pack(pady=10)
stop_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
