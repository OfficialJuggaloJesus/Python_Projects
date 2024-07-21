import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import os

def open_application(app_name):
    try:
        if app_name == "notepad":
            os.system("notepad.exe")
        elif app_name == "calculator":
            os.system("calc.exe")
        else:
            messagebox.showinfo("Info", f"Application '{app_name}' is not recognized.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("Listening", "Listening...")
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)  # Timeout added for testing
            print("Audio captured")
            text = recognizer.recognize_google(audio)
            print(f"Recognized text: {text}")
            messagebox.showinfo("You said", text)
            open_application(text.lower())
        except sr.UnknownValueError:
            messagebox.showwarning("Error", "Could not understand audio")
            print("Could not understand audio")
        except sr.RequestError as e:
            messagebox.showerror("Error", f"Could not request results; {e}")
            print(f"Could not request results; {e}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            print(f"An error occurred: {e}")

def create_gui():
    root = tk.Tk()
    root.title("AI Application Opener")

    label = tk.Label(root, text="Press the button and say the application name:")
    label.pack(pady=10)

    button = tk.Button(root, text="Speak", command=listen)
    button.pack(pady=20)

    root.geometry("300x200")
    root.mainloop()

if __name__ == "__main__":
    create_gui()
