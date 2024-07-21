import tkinter as tk
from tkinter import scrolledtext
import subprocess
import os
import shutil
import platform

class TerminalEmulator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Terminal Emulator")
        self.geometry("600x400")

        self.output_text = scrolledtext.ScrolledText(self, wrap=tk.WORD)
        self.output_text.pack(expand=True, fill=tk.BOTH)

        self.input_frame = tk.Frame(self)
        self.input_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.prompt_label = tk.Label(self.input_frame, text=">>> ")
        self.prompt_label.pack(side=tk.LEFT)

        self.input_entry = tk.Entry(self.input_frame, width=50)
        self.input_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.input_entry.focus_set()

        self.input_entry.bind("<Return>", self.process_command)

        self.command_history = []
        self.history_index = 0

    def process_command(self, event):
        command = self.input_entry.get().strip()
        self.output_text.configure(state=tk.NORMAL)
        self.output_text.insert(tk.END, f">>> {command}\n")

        try:
            if command.lower() == "exit":
                self.quit()
            elif command.lower() == "clear":
                self.output_text.delete(1.0, tk.END)
            elif command.lower().startswith("echo "):
                self.output_text.insert(tk.END, f"{command[5:]}\n")
            elif command.lower().startswith("dir"):
                directory = command[3:].strip()
                output = subprocess.check_output(["dir", directory] if directory else ["dir"], shell=True, universal_newlines=True)
                self.output_text.insert(tk.END, f"{output}\n")
            elif command.lower().startswith("cd "):
                directory = command[3:].strip(' "')
                os.chdir(directory)
                self.output_text.insert(tk.END, f"Changed directory to {os.getcwd()}\n")
            elif command.lower() == "cls":
                self.output_text.delete(1.0, tk.END)
            elif command.lower().startswith("type "):
                file_path = command[5:].strip(' "')
                with open(file_path, 'r') as f:
                    content = f.read()
                    self.output_text.insert(tk.END, f"{content}\n")
            elif command.lower().startswith("del "):
                file_path = command[4:].strip(' "')
                os.remove(file_path)
                self.output_text.insert(tk.END, f"Deleted {file_path}\n")
            elif command.lower().startswith("copy "):
                source, destination = command[5:].strip().split()
                shutil.copy(source, destination)
                self.output_text.insert(tk.END, f"Copied {source} to {destination}\n")
            elif command.lower().startswith("ren "):
                old_name, new_name = command[4:].strip().split()
                os.rename(old_name, new_name)
                self.output_text.insert(tk.END, f"Renamed {old_name} to {new_name}\n")
            elif command.lower().startswith("mkdir "):
                directory = command[6:].strip(' "')
                os.mkdir(directory)
                self.output_text.insert(tk.END, f"Created directory {directory}\n")
            elif command.lower().startswith("rmdir "):
                directory = command[6:].strip(' "')
                os.rmdir(directory)
                self.output_text.insert(tk.END, f"Removed directory {directory}\n")
            elif command.lower().startswith("move "):
                source, destination = command[5:].strip().split()
                shutil.move(source, destination)
                self.output_text.insert(tk.END, f"Moved {source} to {destination}\n")
            elif command.lower().startswith("attrib "):
                args = command[7:].strip()
                subprocess.check_output(["attrib", args], shell=True)
                self.output_text.insert(tk.END, f"Changed attributes: {args}\n")
            elif command.lower().startswith("tasklist"):
                output = subprocess.check_output(["tasklist"], shell=True, universal_newlines=True)
                self.output_text.insert(tk.END, f"{output}\n")
            elif command.lower().startswith("taskkill "):
                task_id = command[9:].strip()
                subprocess.check_output(["taskkill", "/F", "/PID", task_id], shell=True)
                self.output_text.insert(tk.END, f"Killed task with PID {task_id}\n")
            elif command.lower() == "systeminfo":
                output = subprocess.check_output(["systeminfo"], shell=True, universal_newlines=True)
                self.output_text.insert(tk.END, f"{output}\n")
            elif command.lower().startswith("ping "):
                target = command[5:].strip()
                output = subprocess.check_output(["ping", target], shell=True, universal_newlines=True)
                self.output_text.insert(tk.END, f"{output}\n")
            elif command.lower() == "ipconfig":
                output = subprocess.check_output(["ipconfig"], shell=True, universal_newlines=True)
                self.output_text.insert(tk.END, f"{output}\n")
            elif command.lower() == "hostname":
                output = subprocess.check_output(["hostname"], shell=True, universal_newlines=True)
                self.output_text.insert(tk.END, f"{output}\n")
            elif command.lower() == "whoami":
                output = subprocess.check_output(["whoami"], shell=True, universal_newlines=True)
                self.output_text.insert(tk.END, f"{output}\n")
            elif command.lower() == "date":
                output = subprocess.check_output(["date"], shell=True, universal_newlines=True)
                self.output_text.insert(tk.END, f"{output}\n")
            elif command.lower() == "time":
                output = subprocess.check_output(["time"], shell=True, universal_newlines=True)
                self.output_text.insert(tk.END, f"{output}\n")
            elif command.lower() == "uptime":
                if platform.system() == "Windows":
                    output = subprocess.check_output("net statistics server", shell=True, universal_newlines=True)
                else:
                    output = subprocess.check_output("uptime", shell=True, universal_newlines=True)
                self.output_text.insert(tk.END, f"{output}\n")
            elif command.lower() == "diskusage":
                if platform.system() == "Windows":
                    output = subprocess.check_output("fsutil volume diskfree c:", shell=True, universal_newlines=True)
                else:
                    output = subprocess.check_output("df -h", shell=True, universal_newlines=True)
                self.output_text.insert(tk.END, f"{output}\n")
            elif command.lower().startswith("echoargs "):
                args = command[9:].strip()
                self.output_text.insert(tk.END, f"{args}\n")
            elif command.lower().startswith("open "):
                file_path = command[5:].strip(' "')
                if platform.system() == "Windows":
                    os.startfile(file_path)
                elif platform.system() == "Darwin":  # macOS
                    subprocess.Popen(["open", file_path])
                else:  # Linux
                    subprocess.Popen(["xdg-open", file_path])
                self.output_text.insert(tk.END, f"Opened {file_path}\n")
            elif command.lower() == "?":
                available_commands = [
                    "exit: Exit the terminal",
                    "clear: Clear the screen",
                    "echo <text>: Echo back the text",
                    "dir [<directory>]: List files and directories",
                    "cd <directory>: Change current directory",
                    "cls: Clear the screen",
                    "type <file>: Display the contents of a file",
                    "del <file>: Delete a file",
                    "copy <source> <destination>: Copy a file",
                    "ren <old_name> <new_name>: Rename a file",
                    "mkdir <directory>: Create a directory",
                    "rmdir <directory>: Remove a directory",
                    "move <source> <destination>: Move or rename a file or directory",
                    "attrib <args>: Change file attributes",
                    "tasklist: List all running tasks",
                    "taskkill <PID>: Kill a task by its process ID",
                    "systeminfo: Display system information",
                    "ping <target>: Ping a target",
                    "ipconfig: Display IP configuration",
                    "hostname: Display hostname",
                    "whoami: Display current user",
                    "date: Display current date",
                    "time: Display current time",
                    "uptime: Display system uptime",
                    "diskusage: Display disk usage",
                    "echoargs <args>: Echo back the provided arguments",
                    "open <file>: Open a file with the default application"
                ]
                self.output_text.insert(tk.END, "Available commands:\n")
                self.output_text.insert(tk.END, "\n".join(f"  {cmd}" for cmd in available_commands) + "\n")
            else:
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
                self.output_text.insert(tk.END, f"{output}\n")

        except (subprocess.CalledProcessError, FileNotFoundError, OSError) as e:
            self.output_text.insert(tk.END, f"Error: {e}\n")

        self.output_text.configure(state=tk.DISABLED)
        self.output_text.yview(tk.END)

        if command.lower() not in ["?", "clear"]:
            self.command_history.append(command)
            self.history_index = len(self.command_history)
            self.input_entry.delete(0, tk.END)

    def history_up(self, event):
        if self.history_index > 0:
            self.history_index -= 1
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, self.command_history[self.history_index])

    def history_down(self, event):
        if self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, self.command_history[self.history_index])
        elif self.history_index == len(self.command_history) - 1:
            self.history_index = len(self.command_history)
            self.input_entry.delete(0, tk.END)

if __name__ == "__main__":
    app = TerminalEmulator()
    app.bind("<Up>", app.history_up)
    app.bind("<Down>", app.history_down)
    app.mainloop()
