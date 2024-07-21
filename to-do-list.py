import tkinter as tk
from tkinter import messagebox
import json

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")

        self.tasks = []
        self.load_tasks()

        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        self.task_input = tk.Entry(self.frame, width=40)
        self.task_input.pack(side=tk.LEFT, padx=10)

        self.add_task_button = tk.Button(self.frame, text="Add Task", command=self.add_task)
        self.add_task_button.pack(side=tk.LEFT)

        self.listbox = tk.Listbox(root, width=50, height=10)
        self.listbox.pack(pady=10)

        self.delete_task_button = tk.Button(root, text="Delete Task", command=self.delete_task)
        self.delete_task_button.pack()

        self.update_listbox()

    def add_task(self):
        task = self.task_input.get()
        if task:
            self.tasks.append(task)
            self.update_listbox()
            self.save_tasks()
            self.task_input.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "You must enter a task.")

    def delete_task(self):
        try:
            selected_task_index = self.listbox.curselection()[0]
            self.tasks.pop(selected_task_index)
            self.update_listbox()
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("Warning", "You must select a task to delete.")

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            self.listbox.insert(tk.END, task)

    def save_tasks(self):
        try:
            with open("tasks.json", "w") as file:
                json.dump(self.tasks, file, indent=4)
            print("Tasks saved successfully.")
        except Exception as e:
            print(f"Error saving tasks: {e}")

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as file:
                self.tasks = json.load(file)
            print("Tasks loaded successfully.")
        except FileNotFoundError:
            self.tasks = []
            print("No tasks file found. Starting with an empty list.")
        except Exception as e:
            print(f"Error loading tasks: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
