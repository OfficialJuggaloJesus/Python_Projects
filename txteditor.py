import tkinter as tk
from tkinter import filedialog, ttk, messagebox

class TextEditorWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple Text Editor with Tabs")
        self.geometry("800x600")
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")
        
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)
        
        # Set up menus
        self.setup_menu("File", [
            ("New Tab", self.create_tab, "Ctrl+N"),
            ("Open", self.open_file, "Ctrl+O"),
            ("Save", self.save_file, "Ctrl+S"),
            ("Save As...", self.save_file_as, "Ctrl+Shift+S"),
            ("Print", self.print_file, "Ctrl+P"),
            ("Close Tab", self.close_tab, "Ctrl+W"),
            ("", None, ""),
            ("New Window", self.create_new_window, "Ctrl+Shift+N"),
            ("Close Window", self.close_window, "Ctrl+Q"),
            ("", None, ""),
            ("Exit", self.quit, "Alt+F4")
        ])
        
        self.setup_menu("Edit", [
            ("Cut", self.text_operation, "Ctrl+X", "<<Cut>>"),
            ("Copy", self.text_operation, "Ctrl+C", "<<Copy>>"),
            ("Paste", self.text_operation, "Ctrl+V", "<<Paste>>"),
            ("", None, ""),
            ("Select All", self.select_all_text, "Ctrl+A"),
            ("", None, ""),
            ("Find", self.show_dialog, "Ctrl+F", FindReplaceDialog, "Find"),
            ("Replace", self.show_dialog, "Ctrl+R", FindReplaceDialog, "Replace"),
            ("Go To...", self.show_dialog, "Ctrl+G", GoToDialog, "Go To Line")
        ])
        
        # Bind keyboard shortcuts
        self.bind_shortcuts()

        self.create_tab()

    def setup_menu(self, label, items):
        menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=label, menu=menu)
        for item in items:
            if item[0]:
                menu.add_command(label=item[0], command=item[1], accelerator=item[2])
            else:
                menu.add_separator()
    
    def bind_shortcuts(self):
        shortcuts = {
            "<Control-n>": lambda event: self.create_tab(),
            "<Control-o>": lambda event: self.open_file(),
            "<Control-s>": lambda event: self.save_file(),
            "<Control-S>": lambda event: self.save_file_as(),
            "<Control-p>": lambda event: self.print_file(),
            "<Control-w>": lambda event: self.close_tab(),
            "<Control-N>": lambda event: self.create_new_window(),
            "<Control-Q>": lambda event: self.close_window(),
            "<Control-x>": lambda event: self.text_operation(event, "<<Cut>>"),
            "<Control-c>": lambda event: self.text_operation(event, "<<Copy>>"),
            "<Control-v>": lambda event: self.text_operation(event, "<<Paste>>"),
            "<Control-a>": lambda event: self.select_all_text(),
            "<Control-f>": lambda event: self.show_dialog(event, FindReplaceDialog, "Find"),
            "<Control-r>": lambda event: self.show_dialog(event, FindReplaceDialog, "Replace"),
            "<Control-g>": lambda event: self.show_dialog(event, GoToDialog, "Go To Line")
        }
        for key, command in shortcuts.items():
            self.bind_all(key, command)

    def open_file(self, event=None):
        filepath = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not filepath:
            return
        with open(filepath, "r") as input_file:
            text = input_file.read()
        self.create_tab(filepath, text)

    def save_file(self, event=None):
        current_tab = self.notebook.select()
        text_widget = self.notebook.nametowidget(current_tab).text
        filepath = self.notebook.tab(current_tab, 'text')
        if filepath == "Untitled":
            self.save_file_as()
        else:
            self.write_to_file(filepath, text_widget)

    def save_file_as(self, event=None):
        current_tab = self.notebook.select()
        text_widget = self.notebook.nametowidget(current_tab).text
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not filepath:
            return
        self.notebook.tab(current_tab, text=filepath)
        self.write_to_file(filepath, text_widget)

    def write_to_file(self, filepath, text_widget):
        with open(filepath, "w") as output_file:
            text = text_widget.get(1.0, tk.END)
            output_file.write(text)

    def print_file(self):
        current_tab = self.notebook.select()
        text_widget = self.notebook.nametowidget(current_tab).text
        content_to_print = text_widget.get(1.0, tk.END)
        messagebox.showinfo("Print", "Printing content:\n\n" + content_to_print)

    def close_tab(self, event=None):
        current_tab = self.notebook.select()
        self.notebook.forget(current_tab)

    def create_tab(self, title="Untitled", content=""):
        frame = ttk.Frame(self.notebook)
        text_area = tk.Text(frame, wrap="word")
        text_area.insert(tk.END, content)
        text_area.pack(expand=True, fill="both")
        frame.text = text_area  # Store reference to text widget
        self.notebook.add(frame, text=title)
        self.notebook.select(frame)

    def create_new_window(self):
        new_window = TextEditorWindow()
        new_window.mainloop()

    def close_window(self):
        self.destroy()

    def text_operation(self, event=None, operation=None):
        if not operation:
            return
        current_tab = self.notebook.select()
        text_widget = self.notebook.nametowidget(current_tab).text
        text_widget.event_generate(operation)

    def select_all_text(self, event=None):
        current_tab = self.notebook.select()
        text_widget = self.notebook.nametowidget(current_tab).text
        text_widget.tag_add("sel", "1.0", "end")

    def show_dialog(self, event=None, dialog_class=None, title="", *args):
        if not dialog_class:
            return
        dialog = TextEditorDialog(self, dialog_class, title)
        dialog.setup_ui(*args)

class TextEditorDialog(tk.Toplevel):
    def __init__(self, parent, dialog_class, title):
        super().__init__(parent)
        self.parent = parent
        self.dialog_class = dialog_class
        self.title(title)
        self.geometry("300x100")
        
    def setup_ui(self, *args):
        self.dialog_class(self, *args)

class FindReplaceDialog:
    def __init__(self, parent, title):
        self.parent = parent
        self.title = title
        self.setup_ui()

    def setup_ui(self):
        self.label = tk.Label(self.parent, text=f"{self.title}:")
        self.label.pack(pady=5, padx=10, side=tk.LEFT)
        
        self.find_entry = tk.Entry(self.parent, width=30)
        self.find_entry.pack(pady=5, padx=10, side=tk.LEFT)
        
        self.find_button = tk.Button(self.parent, text=self.title, command=self.find)
        self.find_button.pack(pady=5, padx=10, side=tk.LEFT)
        
        self.find_entry.focus_set()

    def find(self):
        find_text = self.find_entry.get()
        current_tab = self.parent.parent.notebook.select()
        text_widget = self.parent.parent.notebook.nametowidget(current_tab).text
        text = text_widget.get("1.0", tk.END)
        
        start_pos = text_widget.search(find_text, "1.0", stopindex=tk.END)
        if start_pos:
            end_pos = f"{start_pos}+{len(find_text)}c"
            text_widget.tag_remove("sel", "1.0", tk.END)
            text_widget.tag_add("sel", start_pos, end_pos)
            text_widget.mark_set("insert", start_pos)
            text_widget.see("insert")
        else:
            messagebox.showinfo(self.title, f"Cannot find '{find_text}'")

class GoToDialog:
    def __init__(self, parent, title):
        self.parent = parent
        self.title = title
        self.setup_ui()

    def setup_ui(self):
        self.label = tk.Label(self.parent, text="Line Number:")
        self.label.pack(pady=5, padx=10, anchor=tk.W)
        
        self.line_number_entry = tk.Entry(self.parent, width=10)
        self.line_number_entry.pack(pady=5, padx=10, anchor=tk.W)
        
        self.go_to_button = tk.Button(self.parent, text=self.title, command=self.go_to_line)
        self.go_to_button.pack(pady=5, padx=10, anchor=tk.W)
        
        self.line_number_entry.focus_set()

    def go_to_line(self):
        line_number = self.line_number_entry.get()
        current_tab = self.parent.parent.notebook.select()
        text_widget = self.parent.parent.notebook.nametowidget(current_tab).text
        text_widget.mark_set("insert", f"{line_number}.0")
        text_widget.see("insert")

if __name__ == "__main__":
    root = TextEditorWindow()
    root.mainloop()
